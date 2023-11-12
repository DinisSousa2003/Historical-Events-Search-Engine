# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd


def run_evaluation(qrels_file, query_url, description):

    # Read qrels to extract relevant documents
    # relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
    # rewrite that line to be ignore lines that start with # and any content after a #
    relevant = [line.strip() for line in open(qrels_file, encoding='utf-8').readlines() if not line.startswith('#') and not line.startswith('\n')]
    relevant = [line.split(' ')[0] for line in relevant]

    # Get query results from Solr instance
    results = requests.get(query_url).json()['response']['docs']

    # METRICS TABLE
    # Define custom decorator to automatically calculate metric based on key
    metrics = {}
    metric = lambda f: metrics.setdefault(f.__name__, f)

    @metric
    def ap(results, relevant):
        """Average Precision"""
        precision_values = []
        relevant_count = 0

        for idx, doc in enumerate(results):
            if doc['event'] in relevant:
                relevant_count += 1
                precision_at_k = relevant_count / (idx + 1)
                precision_values.append(precision_at_k)

        if not precision_values:
            return 0.0

        return sum(precision_values)/len(precision_values)

    @metric
    def p10(results, relevant, n=10):
        """Precision at N"""
        return len([doc for doc in results[:n] if doc['event'] in relevant])/n

    def calculate_metric(key, results, relevant):
        return metrics[key](results, relevant)

    # Define metrics to be calculated
    evaluation_metrics = {
        'ap': 'Average Precision',
        'p10': 'Precision at 10 (P@10)'
    }

    # Calculate all metrics and export results as LaTeX table
    df = pd.DataFrame([['Metric','Value']] +
        [
            [evaluation_metrics[m], calculate_metric(m, results, relevant)]
            for m in evaluation_metrics
        ]
    )

    with open('./evaluation_results/results_' + description + '.tex','w') as tf:
        tf.write(df.to_latex())


    # PRECISION-RECALL CURVE
    # Calculate precision and recall values as we move down the ranked list
    precision_values = [
        len([
            doc
            for doc in results[:idx]
            if doc['event'] in relevant
        ]) / idx
        for idx, _ in enumerate(results, start=1)
    ]

    recall_values = [
        len([
            doc for doc in results[:idx]
            if doc['event'] in relevant
        ]) / len(relevant)
        for idx, _ in enumerate(results, start=1)
    ]

    # precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

    # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
    # recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
    # recall_values = sorted(set(recall_values))

    # extend only after the last recall value if it is less than 1
    if recall_values[-1] < 1:
        recall_values.append(1)
        precision_values.append(precision_values[-1])


    # Extend matching dict to include these new intermediate steps
    # for idx, step in enumerate(recall_values):
    #     if step not in precision_recall_match:
    #         if recall_values[idx-1] in precision_recall_match:
    #             precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
    #         else:
    #             precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]


    # disp = PrecisionRecallDisplay(precision_values, recall_values)
    # disp.plot()
    plt.clf()
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.plot(recall_values, precision_values, linestyle='-', marker='.',)
    plt.savefig('./evaluation_results/precision_recall_' + description + '.pdf')

if __name__ == '__main__':
    descriptions = ['river_18th_century_boosted', 'river_18th_century_base', 'portuguese_as_allies', 'destructive_europe_ww1', 'economic_consequences_revolutions']  # just to keep track of what is what
    qrels_files = ['./qrels/river_18th_century.txt', './qrels/river_18th_century.txt',  './qrels/portuguese_as_allies.txt', './qrels/destructive_europe_ww1.txt', './qrels/economic_consequences_revolutions.txt']
    query_urls = ['http://localhost:8983/solr/conflicts/query?q=label:river%20location:river%20summary:river&q.op=OR&defType=edismax&indent=true&fl=*,%20score&qf=location%5E2%20summary&bq=location:river%5E3&rows=57&fq=date:%5B1700-01-01T00:00:00Z%20TO%201776-01-01T00:00:00Z%5D&useParams=',
    'http://localhost:8983/solr/conflicts/query?q=label:river%20location:river%20summary:river&q.op=OR&indent=true&fl=*,%20score&fq=date:%5B1700-01-01T00:00:00Z%20TO%201776-01-01T00:00:00Z%5D&rows=57&useParams=',
    'http://localhost:8983/solr/conflicts/query?q=summary:portug*%20participants:Portug*&q.op=OR&defType=edismax&indent=true&fl=*,%20score&rows=200&bq=summary:%5C-portug*%20summary:ally%5E5%20summary:allie*%5E5%20summary:portug*%5C-&facet=true&fq=date:%5B1300-01-01T00:00:00Z%20TO%201801-01-01T00:00:00Z%5D&useParams=',
    'http://localhost:8983/solr/conflicts/query?q=summary:destruct*%20%7C%7C%20bomb*%20%7C%7C%20devast*%20%7C%7C%20ruin*%20%7C%7C%20destroy*%20%7C%7C%20damag*&q.op=OR&defType=edismax&indent=true&fl=*,%20score&rows=57&df=summary&fq=date:%5B1914-01-01T00:00:00Z%20TO%201920-01-01T00:00:00Z%5D&fq=summary:engl*%20%7C%7C%20german*%20%7C%7C%20fr*&useParams=',
    'http://localhost:8983/solr/conflicts/query?q=summary:(econom*%5E4%20OR%20rich%20OR%20poor*%20OR%20wealth%20OR%20prosperity%20OR%20depression%5E2%20OR%20recession%5E2%20OR%20inflation%5E2%20OR%20deflation%5E2%20OR%20debt%5E2%20OR%20bankrupt%5E2%20OR%20market*%20OR%20trade*%20OR%20trading%20OR%20commerce%20OR%20commercial%20OR%20merch*%20OR%20industrial%20OR%20industry%20OR%20industries%20OR%20industrialization%20OR%20industrialisation)%0A%0AAND%20(label:revolution*%20OR%20summary:revolution*%20OR%20part_of:revolution*%20OR%20part_of:Revolution*)&q.op=OR&defType=edismax&indent=true&rows=250&fl=*,%20score&qf=part_of%5E2%20label%5E3&bq=part_of:Revolution%5E3%20instance_of:revolution%5E3%20label:Revolution%5E3%20summary:econ*&useParams='

                  ]
    for qrels_file, query_url, description in zip(qrels_files, query_urls, descriptions):
        run_evaluation(qrels_file, query_url, description)

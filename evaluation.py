# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd


def run_evaluation(qrels_file, query_url):

    info_need = qrels_file.split('/')[2].split('.')[0]

    # Read qrels to extract relevant documents
    # relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
    # rewrite that line to be ignore lines that start with # and any content after a #
    relevant = [line.strip() for line in open(qrels_file).readlines() if not line.startswith('#') and not line.startswith('\n')]
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
        return len([doc for doc in results[:n] if doc['id'] in relevant])/n

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

    with open('./evaluation_results/results_' + info_need + '.tex','w') as tf:
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

    precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

    # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
    recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
    recall_values = sorted(set(recall_values))

    # Extend matching dict to include these new intermediate steps
    for idx, step in enumerate(recall_values):
        if step not in precision_recall_match:
            if recall_values[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

    disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
    disp.plot()
    plt.savefig('./evaluation_results/precision_recall_' + info_need + '.pdf')

if __name__ == '__main__':
    qrels_files = ['./qrels/river_18th_century.txt', './qrels/destructive_europe_ww1.txt', './qrels/portuguese_as_allies.txt']
    query_urls = ['http://localhost:8983/solr/conflicts/query?q=label:river%20location:river%20summary:river&q.op=OR&defType=edismax&indent=true&fl=*,%20score&qf=location%5E2%20summary&bq=location:river%5E3&fq=date:%5B1700-01-01T00:00:00Z%20TO%201776-01-01T00:00:00Z%5D&useParams=',
    'http://localhost:8983/solr/conflicts/query?q=label:river%20location:river%20summary:river&q.op=OR&defType=edismax&indent=true&fl=*,%20score&qf=location%5E2%20summary&bq=location:river%5E3&fq=date:%5B1700-01-01T00:00:00Z%20TO%201776-01-01T00:00:00Z%5D&useParams=',
    'http://localhost:8983/solr/conflicts/query?q=label:river%20location:river%20summary:river&q.op=OR&defType=edismax&indent=true&fl=*,%20score&qf=location%5E2%20summary&bq=location:river%5E3&fq=date:%5B1700-01-01T00:00:00Z%20TO%201776-01-01T00:00:00Z%5D&useParams=']

    # the queries are all the same, it is still needed to form good queries for each info need, the river one seems alright but check

    for qrels_file, query_url in zip(qrels_files, query_urls):
        run_evaluation(qrels_file, query_url)

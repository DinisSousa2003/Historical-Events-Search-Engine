# SETUP
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.metrics import PrecisionRecallDisplay, auc
import numpy as np
import json
import requests
import pandas as pd

# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)


def calculate_pr_values(results, relevant):
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

    return recall_values, precision_values


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

    return sum(precision_values) / len(precision_values)

@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['event'] in relevant]) / n


def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)


def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()

    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str


def run_evaluation(qrels_file, query_url, description):
    # if /solr/#/ in query_url: remove the #
    if '/solr/#/' in query_url:
        query_url = query_url.replace('/solr/#/', '/solr/')
    # Read qrels to extract relevant documents
    # relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
    # rewrite that line to be ignore lines that start with # and any content after a #
    relevant = [line.strip() for line in open(qrels_file, encoding='utf-8').readlines() if
                not line.startswith('#') and not line.startswith('\n')]
    relevant = [line.split(' ')[0] for line in relevant]

    # Get query results from Solr instance
    results = requests.get(query_url).json()['response']['docs']

    # Define metrics to be calculated
    evaluation_metrics = {
        'ap': 'Average Precision',
        'p10': 'Precision at 10 (P@10)'
    }

    # Calculate all metrics and export results as LaTeX table
    df = pd.DataFrame([['Metric', 'Value']] +
                      [
                          [evaluation_metrics[m], calculate_metric(m, results, relevant)]
                          for m in evaluation_metrics
                      ]
                      )

    with open('./evaluation_results/tables/results_' + description + '.tex', 'w') as tf:
        tf.write(df.to_latex())

    # write to latex table a table with headers Rank Base if base in description else boosted
    # rank is the order from 1 to 0
    # each row contains if theretrieved document is relevant or not

    df2 = pd.DataFrame([['Rank', 'Base' if 'base' in description else 'Boosted']] + [
        [idx + 1, 'Relevant' if doc['event'] in relevant else 'Not relevant'] for idx, doc in enumerate(results)
    ])

    with open('./evaluation_results/tables/rankings_' + description + '.tex', 'w') as tf:
        tf.write(df2.to_latex())

    # PRECISION-RECALL CURVE
    # Calculate precision and recall values as we move down the ranked list
    recall_values, precision_values = calculate_pr_values(results, relevant)

    plt.clf()
    plt.ylim(0, 1.05)
    plt.xlim(0, 1.05)
    plot_pr_curve(precision_values, recall_values)
    plt.savefig('./evaluation_results/precision_recall_' + description + '.pdf')

    # interpolated
    plt.clf()
    plt.ylim(0, 1.05)
    plt.xlim(0, 1.05)
    plot_interpolated_pr_curve(precision_values, recall_values)
    plt.savefig('./evaluation_results/precision_recall_interpolated_' + description + '.pdf')


def plot_interpolated_pr_curve(precision_values, recall_values, color='#1f77b4'):
    # extend only after the last recall value if it is less than 1
    interpolated_precision_values, extended = interpolate_precision_values(precision_values, recall_values)
    plt.title('Interpolated Precision-Recall Curves', fontweight='bold')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    # plot the markers using the old precision values
    res, = plt.plot(recall_values, interpolated_precision_values, linestyle='-', color=color)

    for idx, step in enumerate(recall_values[:-1 if extended else None]):
        plt.plot(step, precision_values[idx], marker='.', color='#7aa0ac' if color == '#1f77b4' else '#e85c4d')

    return res


def interpolate_precision_values(precision_values, recall_values):
    extended_precision_values = precision_values.copy()
    extended = False
    if recall_values[-1] < 1:
        extended = True
        recall_values.append(1)
        extended_precision_values.append(extended_precision_values[-1])
    # interpolate the precision value
    interpolated_precision_values = []
    for idx, step in enumerate(recall_values):
        interpolated_precision_values.append(max(extended_precision_values[idx:]))
    return interpolated_precision_values, extended


def plot_pr_curve(precision_values, recall_values, color='#1f77b4'):
    plt.title('Precision-Recall Curves')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    # define y axis from 0 to 1
    res, = plt.plot(recall_values, precision_values, linestyle='-', marker='.', color=color)
    return res


def plot_both_pr_curves(description1, description2, qrels_file, query_url1, query_url2):
    if '/solr/#/' in query_url1:
        query_url1 = query_url1.replace('/solr/#/', '/solr/')
    if '/solr/#/' in query_url2:
        query_url2 = query_url2.replace('/solr/#/', '/solr/')

    relevant = [line.strip() for line in open(qrels_file, encoding='utf-8').readlines() if
                not line.startswith('#') and not line.startswith('\n')]
    relevant = [line.split(' ')[0] for line in relevant]

    # Get query results from Solr instance
    results1 = requests.get(query_url1).json()['response']['docs']
    results2 = requests.get(query_url2).json()['response']['docs']


    # PRECISION-RECALL CURVE
    # Calculate precision and recall values as we move down the ranked list
    recall_values1, precision_values1 = calculate_pr_values(results1, relevant)
    recall_values2, precision_values2 = calculate_pr_values(results2, relevant)

    plt.clf()
    plt.ylim(0, 1.05)
    plt.xlim(0, 1.05)
    # set color

    plot1 = plot_pr_curve(precision_values1, recall_values1)
    plot2 = plot_pr_curve(precision_values2, recall_values2, color='#e83d2a')
    plt.legend([plot1, plot2],['Boosted', 'Base'])
    plt.savefig('./evaluation_results/precision_recall_both_' + description1.replace('_boosted', '') + '.pdf')

    plt.clf()
    plt.ylim(0, 1.05)
    plt.xlim(0, 1.05)
    plot3 = plot_interpolated_pr_curve(precision_values1, recall_values1)
    plot4 = plot_interpolated_pr_curve(precision_values2, recall_values2, color='#e83d2a')
    plt.legend([plot3, plot4], ['Boosted system', 'Base system'])
    plt.savefig('./evaluation_results/precision_recall_interpolated_both_' + description1.replace('_boosted', '') + '.pdf')



def plot_boosted_against_semantic(description, qrels_file, query_url):

    if '/solr/#/' in query_url:
        query_url = query_url.replace('/solr/#/', '/solr/')

    post_url ='http://localhost:8983/solr/conflicts/select'

    relevant = [line.strip() for line in open(qrels_file, encoding='utf-8').readlines() if
                not line.startswith('#') and not line.startswith('\n')]
    relevant = [line.split(' ')[0] for line in relevant]

    # Get query results from Solr instance
    results1 = requests.get(query_url).json()['response']['docs']

    # for results2, extract the parameters from the get url used above to send a post request.
    # In the "q" field create the embedding with text_to_embedding

    get_query_params = query_url.split('?')[1].split('&')
    params = {}
    for param in get_query_params:
        key, value = param.split('=')
        if not value:
            continue
        # decode value if it is URL encoded
        if '%' in value:
            value = requests.utils.unquote(value)

        params[key] = value

    embedding = text_to_embedding(params['q'])
    data = {
        "q": f"{{!knn f=vector topK=10}}{embedding}",
    }

    for key, value in params.items():
        if key != 'q':
            data[key] = value

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    results2 = requests.post(post_url, data=data, headers=headers).json()['response']['docs']



    # PRECISION-RECALL CURVE
    # Calculate precision and recall values as we move down the ranked list
    recall_values1, precision_values1= calculate_pr_values(results1, relevant)
    recall_values2, precision_values2 = calculate_pr_values(results2, relevant)

    plt.clf()
    plt.ylim(0, 1.05)
    plt.xlim(0, 1.05)
    # set color

    plot1 = plot_pr_curve(precision_values1, recall_values1)
    plot2 = plot_pr_curve(precision_values2, recall_values2, color='#e83d2a')
    plt.legend([plot1, plot2],['Semantic', 'Boosted'])
    plt.savefig('./evaluation_results/precision_recall_with_semantic_' + description + '.pdf')

    plt.clf()
    plt.ylim(0, 1.05)
    plt.xlim(0, 1.05)
    plot3 = plot_interpolated_pr_curve(precision_values1, recall_values1)
    plot4 = plot_interpolated_pr_curve(precision_values2, recall_values2, color='#e83d2a')
    plt.legend([plot3, plot4], ['Boosted', 'Semantic'])
    plt.savefig('./evaluation_results/precision_recall_interpolated_with_semantic_' + description + '.pdf')

def plot_pr_curve_of_system(qrels_files, query_urls, system, color='#1f77b4'):
    precision_lists = []
    recall_lists = []
    for qrels_file, query_url in zip(qrels_files, query_urls):
        if '/solr/#/' in query_url:
            query_url = query_url.replace('/solr/#/', '/solr/')
        relevant = [line.strip() for line in open(qrels_file, encoding='utf-8').readlines() if
                    not line.startswith('#') and not line.startswith('\n')]
        relevant = [line.split(' ')[0] for line in relevant]

        # Get query results from Solr instance
        results = requests.get(query_url).json()['response']['docs']

        # PRECISION-RECALL CURVE
        # Calculate precision and recall values as we move down the ranked list
        recall_values, precision_values = calculate_pr_values(results, relevant)
        precision_lists.append(interpolate_precision_values(precision_values, recall_values)[0])
        recall_lists.append(recall_values)

    # Initialize arrays to store interpolated precision values for each query
    interpolated_precision_lists = []

    all_recall_values = np.unique(np.concatenate(recall_lists))

    # Interpolate precision values for each query based on the common recall values
    for precision, recall in zip(precision_lists, recall_lists):
        interpolated_precision = np.interp(all_recall_values, recall, precision)
        interpolated_precision_lists.append(interpolated_precision)

    # Calculate average precision for each recall value
    average_precision = np.mean(interpolated_precision_lists, axis=0)

    # Calculate area under the curve (AUC)
    auc_score = auc(all_recall_values, average_precision)

    # Plot the average precision-recall curve
    plt.plot(all_recall_values, average_precision, color=color)


def plot_system_comparison(qrels_files, query_urls):
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Average Precision-Recall Curves', fontweight='bold')
    plt.xlim(0, 1.01)
    plt.ylim(0, 1.01)
    plot_pr_curve_of_system(qrels_files[::2], query_urls[::2], 'Boosted')
    plot_pr_curve_of_system(qrels_files[1::2], query_urls[1::2], 'Base', color='#e83d2a')
    plt.legend(['Boosted system', 'Base system'])
    # plt.show()
    plt.savefig('./evaluation_results/systems_comparison.pdf')


if __name__ == '__main__':
    descriptions = ['river_18th_century_boosted', 'river_18th_century_base',
                    'portuguese_as_allies_boosted', 'portuguese_as_allies_base',
                    'destructive_europe_ww1_boosted', 'destructive_europe_ww1_base',
                    'economic_consequences_revolutions_boosted', 'economic_consequences_revolutions_base'
                    ]
    qrels_files = ['./qrels/river_18th_century.txt', './qrels/river_18th_century.txt',
                   './qrels/portuguese_as_allies.txt', './qrels/portuguese_as_allies.txt',
                   './qrels/destructive_europe_ww1.txt', './qrels/destructive_europe_ww1.txt',
                   './qrels/economic_consequences_revolutions.txt', './qrels/economic_consequences_revolutions.txt'
                   ]
    query_urls = [
        'http://localhost:8983/solr/#/conflicts/query?q=river&q.op=OR&defType=edismax&indent=true&fl=*,%20score&rows=100&df=summary&qf=summary%20participants%5E2%20%20location%5E2%20label%5E2&wt=json&debugQuery=true&debug.explain.structured=true&fq=date:%5B1700-01-01T00:00:00Z%20TO%201776-01-01T00:00:00Z%5D&useParams=',
        'http://localhost:8983/solr/#/conflicts/query?q=river&q.op=OR&defType=edismax&indent=true&fl=*,%20score&rows=57&df=summary&qf=summary%20location%20label%20participants&wt=json&debugQuery=true&debug.explain.structured=true&fq=date:%5B1700-01-01T00:00:00Z%20TO%201776-01-01T00:00:00Z%5D&useParams=',

        'http://localhost:8983/solr/#/conflicts/query?q=portugal&q.op=OR&defType=edismax&indent=true&rows=200&bq=allied~3%5E3%20participants_count:%5B3%20TO%20*%5D%5E7&wt=json&qf=summary%20participants%5E2%20%20location%5E2%20label%5E2&fl=*,%20score&debugQuery=true&debug.explain.structured=true&df=summary&fq=date:%5B1300-01-01T00:00:00Z%20TO%201801-01-01T00:00:00Z%5D&useParams=&qt=',
        'http://localhost:8983/solr/#/conflicts/query?q=portugal&q.op=OR&defType=edismax&indent=true&rows=200&wt=json&qf=summary%20location%20label%20participants&fl=*,%20score&debugQuery=true&debug.explain.structured=true&df=summary&fq=date:%5B1300-01-01T00:00:00Z%20TO%201801-01-01T00:00:00Z%5D&useParams=&qt=',

        'http://localhost:8983/solr/#/conflicts/query?q=destruction%20ruins%20bomb*%20devastat*%20destroy*%20damaging&q.op=OR&defType=edismax&indent=true&fl=*,%20score&rows=100&bq=fort*%5E3%20bombard*%5E5%20bridge%5E5%20city%5E5%20terrain%5E4%20village%5E5%20devastated%5E7%20ruins%5E7%20severely%5E2%20enormous%5E2&qf=summary%20participants%5E2%20%20location%5E2%20label%5E2&df=summary&fq=date:%5B1914-01-01T00:00:00Z%20TO%201920-01-01T00:00:00Z%5D&fq=part_of:(%22war%201%22%20OR%20%22war%20I%22%20OR%20%22great%20war%22%20OR%20%22world%20war%22)%20OR%20summary:(%22war%201%22%20OR%20%22war%20I%22%20OR%20%22great%20war%22%20OR%20%22world%20war%22)&fq=summary:(europe%20OR%20italy%20OR%20germany%20OR%20france%20OR%20britain%20OR%20united%20kingdom%20OR%20belgium%20OR%20poland%20OR%20austria%20OR%20hungary%20OR%20russia)%20%20OR%20location:%20(europe%20OR%20italy%20%20OR%20germany%20OR%20france%20OR%20britain%20OR%20united%20kingdom%20OR%20belgium%20OR%20poland%20OR%20austria%20OR%20hungary%20OR%20russia)%20%20%20%20%20OR%20country:%20(europe%20OR%20italy%20OR%20germany%20OR%20france%20OR%20britain%20OR%20united%20kingdom%20OR%20belgium%20OR%20poland%20OR%20austria%20OR%20hungary%20OR%20russia)&useParams=',
        'http://localhost:8983/solr/#/conflicts/query?q=destruction%20ruins%20bomb*%20devastat*%20destroy*%20damaging&q.op=OR&defType=edismax&indent=true&fl=*,%20score&rows=100&qf=summary%20location%20label%20participants&fq=date:%5B1914-01-01T00:00:00Z%20TO%201920-01-01T00:00:00Z%5D&df=summary&fq=part_of:(%22war%201%22%20OR%20%22war%20I%22%20OR%20%22great%20war%22%20OR%20%22world%20war%22)%20OR%20summary:(%22war%201%22%20OR%20%22war%20I%22%20OR%20%22great%20war%22%20OR%20%22world%20war%22)&fq=summary:(europe%20OR%20italy%20OR%20germany%20OR%20france%20OR%20britain%20OR%20united%20kingdom%20OR%20belgium%20OR%20poland%20OR%20austria%20OR%20hungary%20OR%20russia)%20%20OR%20location:%20(europe%20OR%20italy%20%20OR%20germany%20OR%20france%20OR%20britain%20OR%20united%20kingdom%20OR%20belgium%20OR%20poland%20OR%20austria%20OR%20hungary%20OR%20russia)%20%20%20%20%20OR%20country:%20(europe%20OR%20italy%20OR%20germany%20OR%20france%20OR%20britain%20OR%20united%20kingdom%20OR%20belgium%20OR%20poland%20OR%20austria%20OR%20hungary%20OR%20russia)&useParams=',

        'http://localhost:8983/solr/#/conflicts/query?q=economy&q.op=OR&defType=edismax&indent=true&rows=250&fl=*,%20score&qf=summary%20participants%5E2%20%20location%5E2%20label%5E2&df=summary&bq=part_of:Revolution%5E3%20instance_of:revolution%5E3%20label:Revolution%5E3%20summary:consequence&wt=json&fq=label:revolution*%20OR%20summary:revolution*%20OR%20part_of:revolution*%20OR%20part_of:Revolution*&useParams=',
        'http://localhost:8983/solr/#/conflicts/query?q=economy&q.op=OR&defType=edismax&indent=true&rows=250&fl=*,%20score&qf=summary%20location%20label%20participants&df=summary&wt=json&fq=label:revolution*%20OR%20summary:revolution*%20OR%20part_of:revolution*%20OR%20part_of:Revolution*&useParams='

    ]
    # for qrels_file, query_url, description in zip(qrels_files, query_urls, descriptions):
    #     run_evaluation(qrels_file, query_url, description)
    #
    # for i in range(0, len(descriptions), 2):
    #     plot_both_pr_curves(descriptions[i], descriptions[i + 1], qrels_files[i], query_urls[i], query_urls[i + 1])

    for i in range(0, len(descriptions), 2):
        plot_boosted_against_semantic(descriptions[i], qrels_files[i], query_urls[i])

    # plot_system_comparison(qrels_files, query_urls)



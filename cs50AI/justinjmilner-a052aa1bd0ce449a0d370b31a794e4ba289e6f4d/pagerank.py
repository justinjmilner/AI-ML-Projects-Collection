import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    model = {}
    links = len(corpus[page])

    for pg in corpus:
            model[pg] = (1 - damping_factor) / len(corpus)

    if links:
        for link in corpus[page]:
            model[link] += damping_factor / links

    else:
        for pg in corpus:
            model[pg] = damping_factor / len(corpus)

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Establish a model with each page and a selection count
    model = {}

    for page in corpus:
        model[page] = 0

    # Select random page
    page = random.choice(list(corpus.keys()))

    # Increment the selected page count
    model[page] += (1 / n)

    for i in range(1, n):

        # Determine next transition model
        current_model = transition_model(corpus, page, damping_factor)

        # Select likely page based on page transition model weight
        page = random.choices(list(model.keys()), list(current_model.values()), k=1)[0]

        model[page] += (1 / n)

    return model


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    model = {}

    # Initialize the page values
    for page in corpus:
        model[page] = (1 / len(corpus))

    while True:

        # Make a copy of the model to compare decimal change
        value_checks = 0
        model0 = model.copy()

        # If the page has links add all links
        for page in model:
            sum = 0
            for page3 in model:
                if page in corpus[page3]:
                    sum += model[page3] / len(corpus[page3])
            model[page] = ((1 - damping_factor) / len(model)) + (damping_factor * sum)

        for page in model:
            if abs(model[page] - model0[page]) < .001:
                value_checks += 1
                if value_checks == len(model):
                    return model


if __name__ == "__main__":
    main()

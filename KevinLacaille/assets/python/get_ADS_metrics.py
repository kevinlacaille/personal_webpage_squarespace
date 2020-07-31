#!/usr/bin/python3
class AdsMetrics:

    def __init__(self, author, metrics):
        ''' The constructor.

        Args:
            self    - The class object
            author  - The author name.
                      Format: Last, First
                      Type: String
            metrics - The metrics to be measured.
                      Format: ['metric1', 'metric2', ..., 'metricN']
                      Type: List

        Returns:
            None

        Raises:
            TypeError: The inputed <Type> for <Arg> `<inputed Arg>' does not match the required format.
        '''

        # Check for input types
        if not isinstance(author, str):
            raise TypeError("The inputed string for author name `{}".format(author) + "' does not match the required format.")
        if not isinstance(metrics, list):
            raise TypeError("The inputed list for requested metrics `{}".format(metrics) + "' does not match the required format.")
        for metric in metrics:
            if not isinstance(metric, str):
                raise TypeError("The inputed string for requested metric `{}".format(metric) + "' does not match the required format.")

        # Set author and metrics
        self.author = author
        self.metrics = metrics


    def get_ads_metrics(self) -> int:
        ''' Obtains requested metrics from ADS.

        Args:
            self - The class object.

        Returns:
            None

        Raises:
            None
        '''
        from os.path import isfile

        # Import and set development key for ADS
        ADS_DEV_KEY_file = "ADS_DEV_KEY.txt"
        if not isfile(ADS_DEV_KEY_file):
            raise FileNotFoundError()

        import ads

        ADS_DEV_KEY = open(ADS_DEV_KEY_file).read().rstrip("\n")

        ads.config.token = ADS_DEV_KEY

        # All papers with Lacaille, K as an author
        all_papers = list(ads.SearchQuery(author=self.author, fl=[self.metrics]))

        # Find total citations and reads for each paper, and which has been refereed
        total_citations = 0
        total_reads = 0
        n_papers_unrefereed = 0

        for paper in all_papers:
            total_citations += paper.citation_count
            total_reads += paper.read_count
            if paper.pub == 'arXiv e-prints':
                n_papers_unrefereed += 1
            
        n_papers_total = len(all_papers)
        n_papers_refereed = n_papers_total - n_papers_unrefereed


        print("Total citations is {}".format(total_citations), 
              "Total reads is {}".format(total_reads), 
              "Total refereed papers is {}".format(n_papers_refereed))
        return total_citations, total_reads, n_papers_refereed


if __name__ == "__main__":
    
    adsMetrics = AdsMetrics("Lacaille, K", ['citation_count', 'read_count', 'pub'])
    adsMetrics.get_ads_metrics()
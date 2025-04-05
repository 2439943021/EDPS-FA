# coding=utf-8

class PubmedEntity:
    def __init__(self, paper_id='', title='', date='', author_list='', journal='', abstract='', free_label='',
                 links_dict='',
                 doi_id='',
                 pm_id='', pmc_id=''):
        self.paper_id = paper_id
        self.title = title
        self.date = date
        self.author_list = author_list
        self.journal = journal
        self.abstract = abstract
        self.free_label = free_label
        self.links_dict = links_dict
        self.doi_id = doi_id
        self.pm_id = pm_id
        self.pmc_id = pmc_id
        self.is_success = True
        self.download_type = ''
        self.download_path = ''
        self.download_url = ''
        self.pdf_pubmed_url = ''
        self.pdf_oss_url = ''
        self.info = ''

    def print_info(self):
        print(f"Paper ID: {self.paper_id}")
        print(f"Title: {self.title}")
        print(f"date: {self.date}")
        print(f"Author List: {self.author_list}")
        print(f"journal: {self.journal}")
        print(f"Abstract: {self.abstract}")
        print(f"Free Label: {self.free_label}")
        print(f"Links Dict: {self.links_dict}")
        print(f"DOI ID: {self.doi_id}")
        print(f"PM ID: {self.pm_id}")
        print(f"PMC ID: {self.pmc_id}")
        print(f"Is Success: {self.is_success}")
        print(f"Download Type: {self.download_type}")
        print(f"Download Path: {self.download_path}")
        print(f"Info: {self.info}")

    def to_dict(self):
        """
        将 PubmedEntity 对象转换为字典
        @return:
        """
        entity_dict = {
            "paper_id": self.paper_id,
            "title": self.title,
            "date": self.date,
            "author_list": self.author_list,
            "journal": self.journal,
            "abstract": self.abstract,
            "free_label": self.free_label,
            "links_dict": self.links_dict,
            "doi_id": self.doi_id,
            "pm_id": self.pm_id,
            "pmc_id": self.pmc_id,
            "is_success": self.is_success,
            "download_type": self.download_type,
            "download_path": self.download_path,
            "info": self.info
        }
        return entity_dict

    @staticmethod
    def dict_to_entity(pubDict):
        """
        将json字段转为实体
        @rtype: object
        """
        pubmed_entity = PubmedEntity()
        pubmed_entity.paper_id = pubDict['paper_id']
        pubmed_entity.title = pubDict['title']
        pubmed_entity.date = pubDict['date']
        pubmed_entity.author_list = pubDict['author_list']
        pubmed_entity.journal = pubDict['journal']
        pubmed_entity.abstract = pubDict['abstract']
        pubmed_entity.free_label = pubDict['free_label']
        pubmed_entity.links_dict = pubDict['links_dict']
        pubmed_entity.doi_id = pubDict['doi_id']
        pubmed_entity.pm_id = pubDict['pm_id']
        pubmed_entity.pmc_id = pubDict['pmc_id']
        pubmed_entity.is_success = pubDict['is_success']
        pubmed_entity.download_type = pubDict['download_type']
        pubmed_entity.download_path = pubDict['download_path']
        pubmed_entity.info = pubDict['info']
        return pubmed_entity


if __name__ == '__main__':
    print('Python')

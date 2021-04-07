# By: Emily Cao and Jina Kim

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    root_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(root_path, filename)

    #open the file
    with open(filepath, 'r', encoding="utf-8") as f:
        search_results_text = f.read()

    #create soup object
    soup = BeautifulSoup(search_results_text, "html.parser")
    search_results_table = soup.find('table', class_ = 'tableList')
    table = search_results_table.find_all('tr')

    #find author name and book titles
    newList = []
    for row in table:
        #get book title
        book = row.find('a', class_ = "bookTitle")
        bookTitle = book.text.strip()

        #get author name
        author = row.find('a', class_ = 'authorName')
        authorName = author.find('span').text.strip()
        newList.append((bookTitle, authorName))
  
    # print(newList)
    return newList


    # pass


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    resp = requests.get(url)
    if resp.ok:
        soup = BeautifulSoup(resp.text, 'html.parser')
        newList = []
        left = soup.find("div", class_ = "leftContainer")
        table = left.find("table", class_ = "tableList")
        rows = table.find_all("tr")
        starter = "https://www.goodreads.com"

        for row in rows[0:10]:
        # link = row.find("a", href = True)
        # new_starter = starter + link['href']
            link = row.find("a").get("href", None).strip()
            new_starter = starter + link
            newList.append(new_starter)
        return newList
    # print (newList)
    


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    resp = requests.get(book_url)
    # print(book_url)
    if resp.ok:
        soup = BeautifulSoup(resp.text, 'html.parser')
    # newList = []
        body = soup.find("div", class_ = "content")
        main = body.find("div", class_ = "mainContentContainer")
    # print(main)
        content = main.find("div", class_= "mainContent")
        left = content.find("div", class_ = "leftContainer")
    # print(left)
        column = left.find("div", id = "topcol")
    
        new_column = column.find("div", id = "metacol")

        bookTitle = new_column.find("h1", id = "bookTitle").text.strip()

        author_id = new_column.find("div", id = "bookAuthors")
        authorName = author_id.find('a', class_ = 'authorName').text.strip()
    

        number = new_column.find("div", id = "details")
        pages = number.find('span', itemprop = 'numberOfPages')
  
        pagesNumber = re.search(r'\b\d+\b', pages.text.strip()).group(0)

        a_tup = (bookTitle, authorName, int(pagesNumber))
    
    return a_tup
    


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    root_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root_path, filepath)

    #open the file
    with open(path, 'r') as f:
        summarize_best_books = f.read()

    #create soup object
    newList = []
    soup = BeautifulSoup(summarize_best_books, "html.parser")
    container = soup.find("div", class_ = 'categoryContainer')
    category = container.find_all('div', class_ = 'category clearFix')
    

    for x in category:
        # copy = x.find('h4', class_ = 'category__copy')
        # genre = copy.text.strip() 
        genre = x.find('h4', class_ = 'category__copy').text.strip()

        # image = x.find('img', alt = True)
        # bookTitle = image['alt']
        bookTitle = x.find('img').get('alt', None).strip()
        # print(bookTitle)

        url = x.find('a').get('href', None).strip()
        # a_url = x.find('a', href = True)
        # url = a_url['href']
        # print(url)

        x = (genre, bookTitle, url)
        newList.append(x)
    return newList
    # print(newList)


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w', newline = '') as f:
        writer = csv.writer(f,delimiter = ",")
        writer.writerow(('Book title', 'Author Name'))
        writer.writerows(data)
        


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.

    USE REGEX!

    For the purposes of this assignment, we will define a named entity as follows:

●   Named entities contain 2 or more capitalized words, with no lowercase words in-between them
●   The words must be separated by spaces 
●   The first word must contain at least 3 letters

Write a new function extra_credit() that takes a single filepath parameter. 
It should create a BeautifulSoup object from the filepath, given that filepath corresponds to the webpage for a
book on Goodreads.com. Extract the description** of the book from the BeautifulSoup object and find all the named
entities (using the criteria given above) within the book description. This function should return a list of all 
named entities present in the book description for the given filepath. Your list should be in the following format: 

[‘Named Entity_1’, ‘Named Entity_2, …..]

    """
    root_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(root_path, filepath)

    #open the file
    with open(path, 'r') as f:
        extra_cred = f.read()
    soup = BeautifulSoup(extra_cred, 'html.parser')
    description = soup.find('div', id = 'description').text.strip()
    entities = re.findall(r'\b[A-Z]\w{2}\w*(?: [A-Z]\w*\b)+', description)
    return entities
    # print(entities)



class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results("search_results.htm")

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)

        # check that the variable you saved after calling the function is a list    
        self.assertEqual(type(titles), list)

        # check that each item in the list is a tuple
        for x in titles:
            self.assertEqual(type(x), tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(titles[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"))
        # self.assertEqual(titles[0][0], "Harry Potter and the Deathly Hallows (Harry Potter #7)")
        # self.assertEqual(titels[0][1], "J.K. Rowling")
                                     
        # check that the last title is correct (open search_results.htm and find it)  
        self.assertEqual(titles[-1][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        # self.assertEqual(titles[-1][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        # self.assertEqual(titels[-1][1], "J.K. Rowling")



    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for x in TestCases.search_urls:
            self.assertEqual(type(x), str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for x in TestCases.search_urls:
            self.assertEqual('https://www.goodreads.com/book/show/' in x, True)

        # reg_exp = r'^https:\/\/www\.goodreads\.com\/book\/show\/.+'
        # for x in TestCases.search_urls:
        #     y = str(re.findall(reg_exp, x))
        #     string = y.replace("'", "")
        #     string1 = string.replace("[", "")
        #     string2 = string1.replace("]", "")
        #     self.assertEqual(string2, x)


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for x in TestCases.search_urls:
            a_summary = get_book_summary(x)
            summaries.append(a_summary)

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

            # check that each item in the list is a tuple
        for a_tuple in summaries:
            self.assertEqual(type(a_tuple), tuple)

            # check that each tuple has 3 elements
            self.assertEqual(len(a_tuple), 3)

            # check that the first two elements in the tuple are string
            self.assertEqual(type(a_tuple[0]), str)
            self.assertEqual(type(a_tuple[1]), str)

            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(a_tuple[2]), int)

        # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)
        

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summary1 = summarize_best_books("best_books_2020.htm")

        # check that we have the right number of best books (20)
        self.assertEqual(len(summary1), 20)
    
            # assert each item in the list of best books is a tuple
        for x in summary1:
            self.assertEqual(type(x), tuple)

            # check that each tuple has a length of 3
            self.assertEqual(len(x), 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(summary1[0], ('Fiction','The Midnight Library', 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(summary1[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        a_list = get_titles_from_search_results('search_results.htm')

        # call write csv on the variable you saved and 'test.csv'
        write_csv(a_list, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        # f = open('test.csv', 'r')
        # csv_lines = list(csv.reader(f))
        # f.close()
        # print(csv_lines)
        with open('test.csv') as file:
            csv_lines = list(csv.reader(file))
        # print(csv_lines)
        
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book title', 'Author Name'])

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])


    def test_extra_credit(self):
        ec = extra_credit("extra_credit.htm")
        # went to office hours and the amount is suppose to be 10, not 9 -> include "For Moscow"
        self.assertEqual(len(ec), 10)
        

if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)
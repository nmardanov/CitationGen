# CitationGen
Online citation generator project made for my IB SL Computer Science Internal Assessment as an alternative to sites like BibMe, which are often filled with ads or 
paywalls.

Includes files for a website & Python script that can generate MLA format citations given a website URL. Uses BeautifulSoup4 to access site data.
If you want to run this locally, you might need to edit some filepaths. For instance, the path to python in the test.php file, and make sure that you set the path to
the htdocs folder locally, if you're using XAMPP to run a server.

WARNING: Some websites will refuse to connect, but most should work fine. This is because of the headers used by the script, which connects through the Python requests
 library. Also, this project isn't totally finished or polished, but most of the functionality is ready. This serves more as a proof-of-concept to be developed further
 in the future. 

# Hambaanglaang Storybooks

## 2022-07-31

This is a GitHub release of Hambaanglanag Cantonese storybooks for language processing work. We want to create a machine-friendly dataset with our existing stories, including text, jyutping, gloss, image and audio recordings, and set up automatic, continuous integration to generate books, videos, H5P, etc. with the latest dataset. Once this is done, we can easily correct typos, add new languages, change illustrations, etc. without manual intervention. Computer-savvy volunteers will be able to improve the materials by making changes to this centralised, public copy.

`legacy\sheets` contain `.csv` files that were used in the generation of Jyutping panels. 
`legacy\utils\csv2xml.py` converts these legacy csv sheets into [TEI-compliant](https://tei-c.org) XML files. The format has not yet been finalised. Ultimately page breaks (for videos/print), illustrations, per-sentence translations, etc. will be added to the XML file, and contributor information will be updated.

## How to contribute

There is going to be development work involved, please send us a message at info@hambaanglaang.hk if you would like to help.

## License

Hambaanglaang storybooks are released under the [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

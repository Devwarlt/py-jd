# PY-JD: Python JSON Descriptor [![license-badge]][license] [![size-badge]][latest] [![visitors-badge]][latest]
PY-JD is an algorithm written in Python that iterates through all JSON object properties using [Tree Traverse technique](https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder/) and describes distinct information in three different patterns for easy diff check.

## Languages
![python-language-badge]

## Usage

*Consider this JSON input:*

<details>
  
  <summary>sample.json</summary>
  
  ```json
  {
      "glossary": {
          "title": "example glossary",
          "GlossDiv": {
              "title": "S",
              "GlossList": {
                  "GlossEntry": {
                      "ID": "SGML",
                      "SortAs": "SGML",
                      "GlossTerm": "Standard Generalized Markup Language",
                      "Acronym": "SGML",
                      "Abbrev": "ISO 8879:1986",
                      "GlossDef": {
                          "para": "A meta-markup language, used to create markup languages such as DocBook.",
                          "GlossSeeAlso": ["GML", "XML"]
                      },
                      "GlossSee": "markup"
                  }
              }
          }
      }
  }
  ```
  
</details>

Must import references from module `json_descriptor`, see example below:

```python
import json_descriptor
import json


file_path: str = 'sample.json'
with open(file_path, 'r', encoding='utf8') as file:
  content_str: str = file.read()
  content: dict = json.loads(content_str)
  regular_navigation, json_contract, jmespath_list = json_descriptor.get_descriptor_details(content)
  with open(file_path.replace('.json', '-regular_navigation.txt'), 'w', encoding='utf8') as regular_navigation_file:
      regular_navigation_file.write(regular_navigation)
  with open(file_path.replace('.json', '-json_contract.json'), 'w', encoding='utf8') as json_contract_file:
      json_contract_file.write(json_contract)
  with open(file_path.replace('.json', '-jmespath_list.json'), 'w', encoding='utf8') as jmespath_list_file:
      jmespath_list_file.write(jmespath_list)
```

---

**Patterns:**

`Pattern 1 - Regular Navigation`:

<details>
  
  <summary>sample-regular_navigation.txt</summary>
  
  ```txt
  [+] root (type: dict)
  .[+] glossary (type: dict) | (JMESPath: glossary[])
  ..[-] title (type: str) | (JMESPath: glossary[].title)
  ..[+] GlossDiv (type: dict) | (JMESPath: glossary[].GlossDiv[])
  ...[-] title (type: str) | (JMESPath: glossary[].GlossDiv[].title)
  ...[+] GlossList (type: dict) | (JMESPath: glossary[].GlossDiv[].GlossList[])
  ....[+] GlossEntry (type: dict) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[])
  .....[-] ID (type: str) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].ID)
  .....[-] SortAs (type: str) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].SortAs)
  .....[-] GlossTerm (type: str) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossTerm)
  .....[-] Acronym (type: str) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].Acronym)
  .....[-] Abbrev (type: str) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].Abbrev)
  .....[+] GlossDef (type: dict) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossDef[])
  ......[-] para (type: str) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossDef[].para)
  ......[+] GlossSeeAlso (type: list) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossDef[].GlossSeeAlso[])
  .......[-] field of 'GlossSeeAlso' (type: str) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossDef[].GlossSeeAlso[])
  .....[-] GlossSee (type: str) | (JMESPath: glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossSee)
  ```

</details>

`Pattern 2 - JSON Contract`:

<details>
  
  <summary>sample-json_contract.json</summary>
  
  ```json
  {
      "root": [{
          "glossary": [{
                  "title": "str"
              },
              {
                  "GlossDiv": [{
                          "title": "str"
                      },
                      {
                          "GlossList": [{
                              "GlossEntry": [{
                                      "ID": "str"
                                  },
                                  {
                                      "SortAs": "str"
                                  },
                                  {
                                      "GlossTerm": "str"
                                  },
                                  {
                                      "Acronym": "str"
                                  },
                                  {
                                      "Abbrev": "str"
                                  },
                                  {
                                      "GlossDef": [{
                                              "para": "str"
                                          },
                                          {
                                              "GlossSeeAlso": [{
                                                  "field of 'GlossSeeAlso'": "str"
                                              }]
                                          }
                                      ]
                                  },
                                  {
                                      "GlossSee": "str"
                                  }
                              ]
                          }]
                      }
                  ]
              }
          ]
      }]
  }
  ```

</details>

`Pattern 3 - JMESPath List`:

<details>
  
  <summary>sample-jmespath_list.json</summary>
  
  ```json
  [
      "",
      "glossary[]",
      "glossary[].GlossDiv[]",
      "glossary[].GlossDiv[].GlossList[]",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[]",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].Abbrev",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].Acronym",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossDef[]",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossDef[].GlossSeeAlso[]",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossDef[].GlossSeeAlso[]",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossDef[].para",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossSee",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].GlossTerm",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].ID",
      "glossary[].GlossDiv[].GlossList[].GlossEntry[].SortAs",
      "glossary[].GlossDiv[].title",
      "glossary[].title"
  ]
  ```

</details>

### Contributors
- Nádio ~ [@Devwarlt][nadio-ref]
- UnB Back-end Developers ~ Cortex Team

[nadio-ref]: https://github.com/Devwarlt

[latest]: https://github.com/Devwarlt/py-jd

[python-language-badge]: https://img.shields.io/badge/Python-3.8.3-yellow?logo=python&style=plastic
[size-badge]: https://img.shields.io/github/repo-size/Devwarlt/r2md?style=plastic
[visitors-badge]: https://visitor-badge.glitch.me/badge?page_id=Devwarlt.py-jd

[license-badge]: https://img.shields.io/badge/License-WTFPL-black?style=plastic
[license]: /LICENSE

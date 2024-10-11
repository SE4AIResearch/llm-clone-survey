# LLMs in Computer Science Education Survey
This repository contains the code for scraping and processing papers for the LLMs in Computer Science Education literature review. 
This work has been accepted for the 56th ACM Technical Symposium on Computer Science Education (SIGCSE TS 2025).


## Authors
- Nishat Raihan (GMU)
- Mohammed Latif Siddiq (Notre Dame)
- Joanna C. S. Santos (Notre Dame)
- Marcos Zampieri (GMU)

## Accompanying Website
- [LLMs in Computer Science Education Survey](https://llm4csedu.github.io/)
- 
## Abstract
Large language models (LLMs) are becoming increasingly better at a wide range of Natural Language Processing tasks (NLP), such as text generation and understanding. Recently, these models have extended their capabilities to coding tasks, bridging the gap between natural languages (NL) and programming languages (PL). Foundational models such as the Generative Pre-trained Transformer (GPT) and LLaMA series have set strong baseline performances in various NL and PL tasks. Additionally, several models have been fine-tuned specifically for code generation, showing significant improvements in code-related applications. Both foundational and fine-tuned models are increasingly used in education, helping students write, debug, and understand code. We present a comprehensive systematic literature review to examine the impact of LLMs in computer science and computer engineering education. We analyze their effectiveness in enhancing the learning experience, supporting personalized education, and aiding educators in curriculum development. We address five research questions to uncover insights into how LLMs contribute to educational outcomes, identify challenges, and suggest directions for future research.

## Pre-requisites
- Python 3.11+
- pip
- git
- Dependencies on requirements.txt


## Folders

- `data`: Contains data used in our survey. It contains the DB dump with our analysis.
- `results`: Contains the results of our scrape scripts. It contains lists of papers collected from different sources.
- `scripts`: Contains the source code for utility scripts to extract/process papers.

## Citation
If you use this code in your research, please cite the following paper:
```
@inproceedings{nishat2025llmeducation,
  author={Raihan, Nishat and Siddiq, Mohammed Latif and Santos, Joanna C. S. and Zampieri, Marcos},
  title={Large Language Models in Computer Science Education: A Systematic Literature Review}, 
  booktitle = {Proceedings of the 56th ACM Technical Symposium on Computer Science Education (SIGCSE TS '25)},
  numpages = {7},
  location = {Pittsburgh, Pennsylvania, United States},
  series = {SIGCSE TS '25}
}
```


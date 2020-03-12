# SYQ1 FYP 19-20

## Links
Date and Tasks Google Docs - https://docs.google.com/document/d/1_hZRVgCpLIr4eRkcN_XUIH37kvFyd-zENGd4lcbqAQQ/edit

Research Notes and Links Google Docs - https://docs.google.com/document/d/1820clrvOzJhBsEIrg_ElYxn46ze_h2oHYOViLXi8RxU/edit


## Other Notes

Please use a Python 3.6+ virtual environment for reproducibility. Install packages based on the requirements.txt, though not all of them may install using 'pip -r requirements.txt'. You may have to remove some of the lines manually. 

Please add stuff to .gitignore as necessary.

Project structure according to https://towardsdatascience.com/manage-your-data-science-project-structure-in-early-stage-95f91d4d0600. 

For neuralcoref package, might need to install it using 'pip3 uninstall neuralcoref; pip3 install neuralcoref --no-binary neuralcoref'. It can also likely only be run on Linux.

If using jupyter lab/notebook, make sure that you configure it correctly so that it uses the virtual environment's python interpreter rather than the systemwide on.

The requirements_old.txt in the main project folder is old, use FewRel/requirements.txt instead. 

To use `models/OpenNRE`, set the `PYTHONPATH` variable to `/path-to/FYP-19-20/models/OpenNRE` in .bashrc. 

If the dependency library `flair` from `requirements.txt` fails to download, try:
```
    pip install --upgrade git+https://github.com/flairNLP/flair.git
```
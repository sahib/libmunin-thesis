.. One big hack.

.. only:: html or singlehtml or singletext

    Abkürzungsverzeichnis
    ======================

.. raw:: latex

    \renewcommand{\thepage}{\roman{page}}
    \setcounter{page}{8} % cough.
    \addcontentsline{toc}{section}{Abk"urzungsverzeichnis}
    {\centering\Huge \textbf{Abk"urzungsverzeichnis}}

.. figtable::
    :spec: >{\raggedleft\arraybackslash}p{0.25\linewidth} p{0.65\linewidth}

    =======================  ==================================
    Abkürzung                Bedeutung
    =======================  ==================================
    **API**                  *Application Programming Interface*
    **GUI**                  *Graphical User Interface*
    **LoC**                  *Lines of Code*
    =======================  ==================================

.. raw:: latex

    % \pagenumbering{arabic}
    \newpage
    \renewcommand{\thepage}{\arabic{page}}
    % \pagestyle{fancy}
    \setcounter{page}{1}

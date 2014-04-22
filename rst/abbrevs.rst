:orphan:

.. One big hack.

.. only:: html or singlehtml or singletext

    **Abkürzungsverzeichnis**

.. raw:: latex

    \thispagestyle{plain}
    \renewcommand{\thepage}{\roman{page}}
    \setcounter{page}{8} % cough.
    \addcontentsline{toc}{section}{Abk"urzungsverzeichnis}
    {%
        \vspace*{2em}
        \Huge\textbf{Abk"urzungsverzeichnis}
        \vspace{1em}
    }%

.. figtable::
    :spec: >{\raggedleft\arraybackslash}p{0,25\linewidth} p{0,65\linewidth}

    =======================  ==================================
    Abkürzung                Bedeutung
    =======================  ==================================
    API                      *Application Programming Interface*
    BPM                      *Beats per Minute*
    FAQ                      *Frequently Asked Questions*
    URL                      *Uniform Resource Locator*
    MP3                      *MPEG-2 Audio Layer III*
    FLAC                     *Free Lossless Audio Codec*
    =======================  ==================================

.. raw:: latex

    \newpage
    \renewcommand{\thepage}{\arabic{page}}
    \pagestyle{fancy}
    \setcounter{page}{1}

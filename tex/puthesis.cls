\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{puthesis}[]
\RequirePackage{setspace}
\RequirePackage{ccicons}
\RequirePackage{ifthen}
\RequirePackage[utf8]{inputenc}

\def\copyrightyear#1{\gdef\@copyrightyear{#1}}
\def\worktitle#1{\gdef\@worktitle{#1}}
\def\worksubtitle#1{\gdef\@worksubtitle{#1}}
\def\adviserstreet#1{\gdef\@adviserstreet{#1}}
\def\advisercity#1{\gdef\@advisercity{#1}}
\def\authorstreet#1{\gdef\@authorstreet{#1}}
\def\authorcity#1{\gdef\@authorcity{#1}}
\def\adviser#1{\gdef\@adviser{#1}}

\newcommand*{\frontmatter}{%
  \pagenumbering{roman}
}%
\newcommand*{\mainmatter}{\pagenumbering{arabic}}
\newcommand*{\makelot}{}
\newcommand*{\makelof}{}
\newcommand*{\makelos}{}
\newcommand*{\maketoc}{%
  % Add ToC to the pdfbookmarks as a section, but not to the ToC itself.
  % only if we have the hyperref command that is necessary
  \ifdefined\pdfbookmark
     \phantomsection
     \pdfbookmark[1]{\contentsname}{Contents}
  \else
  \fi

  \tableofcontents
  \clearpage
}%

%% Setup a command to add extra space only if in singlespacing mode
\newcommand*{\extravspace}[1]{%
    \vspace{0in}
}%

%% Setup a command to set spacing for body text; also used to restore spacing after long tables in document
\newcommand*{\bodyspacing}{%
  \onehalfspacing
}%

%% Setup a command to set spacing for long tables, to be used manually in document
\newcommand*{\tablespacing}{%
  \singlespacing
}%

%% Command inserted into the document immediately after \begin{document} to place all frontmatter
%%   This was formerly named 'begincmd' and called below in \AtBeginDocument{}
%%   However, that is not compatible with package 'hyperref'. \tableofcontents needs
%%   to be declared from within the document itself. 
\newcommand*{\makefrontmatter}{%
    \titlespacing{\chapter}{0pt}{0.0em}{0.2em}
    \bodyspacing
    \frontmatter\maketitlepage\makecopyrightpage\makeabstract
    \maketoc
    \makelot\clearpage\makelof\clearpage\makelos
    \clearpage\mainmatter
    \titlespacing{\chapter}{0pt}{0.0em}{2em}
}% 

\long\def\acknowledgements#1{\gdef\@acknowledgements{#1}}

\newcommand{\maketitlepage}{{%
  \thispagestyle{empty}
  \begin{center}
    \includegraphics[width=150px]{fh_hof_logo.pdf}
  \end{center}
  \vspace{.6in}
  \extravspace{.6in}
  \normalfont\scshape
  \vspace*{0in}
  \begin{center}
    \LARGE \@worktitle \\
    \vspace{.1in}
    \large \@worksubtitle
  \end{center}
  \vspace{.6in}
  \extravspace{.6in}
  \vspace{.6in}
  \extravspace{.6in}
  \begin{center}
    \Large Bachelorarbeit\\
    \large an der Hochschule für Angewandte Wissenschaften Hof \\
  \end{center}
  \vspace{.6in}
  \extravspace{.6in}
  \begin{center}
    Vorgelegt bei: \hfill Vorgelegt von: \\
    \@adviser \hfill  \theauthor \\
    {\small \@adviserstreet \hfill \@authorstreet} \\
    {\small \@advisercity \hfill \@authorcity} \\
  \end{center}
  \vspace{.9in}
  \extravspace{.9in}
  \begin{center}
    Hof, \today
  \end{center}
  \clearpage
}}%

\newcommand*{\makecopyrightpage}{%
  \thispagestyle{empty}
  \vspace*{0in}
  \begin{center}
    {\Large\reflectbox{\huge$_\copyright$}}\ Copyleft by \@author, \@copyrightyear. \\
    Some rights reserved. \\
    \vspace{1in}
    \begin{minipage}[c]{0.2\linewidth}
      \hfill {\Huge \ccLogo~\ccAttribution}
    \end{minipage}
    \hspace{0.1cm}
    \begin{minipage}[c]{0.7\linewidth}
      Diese Arbeit ist unter den Bedingungen der \\
      \textit{Creative Commons Attribution--3.0} lizensiert. \\
      \url{http://creativecommons.org/licenses/by/3.0/de/}
    \end{minipage}
  \end{center}
  \clearpage
}%

%%%% ABSTRACT %%%%%%
\newcommand*{\makeabstract}{%
  \newpage
  \addcontentsline{toc}{section}{Abstract}
  \begin{center}
  \Large \textbf{Abstract}
  \end{center}
  \thispagestyle{empty}
  \@abstract

  \addcontentsline{toc}{section}{Danksagung}
  \begin{center}
    \Large \textbf{Danksagung}
  \end{center}
  \thispagestyle{empty}
  \@acknowledgements
}%


\def\makededication{
  \ifx\@dedication\undefined
  \else
    \vspace*{1.5in}
    \begin{flushright}
      \@dedication
    \end{flushright}
    \thispagestyle{empty}
    \addcontentsline{toc}{section}{Widmung}
    \clearpage
  \fi
  }

\DeclareOption{lof}{\renewcommand*{\makelof}{%
  \ifdefined\phantomsection
    % makes hyperref recognize this section properly for pdf links
    \phantomsection
  \else
  \fi
  \addcontentsline{toc}{section}{Abbildungsverzeichnis}\listoffigures}
}% 

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrreprt}}
\ProcessOptions
\PassOptionsToClass{twoside}{scrreprt}


%% Not necessary to specify the point size - we inherit it from above
\LoadClass{scrreprt}
\setlength{\oddsidemargin}{.5in}   %{.4375in}
\setlength{\evensidemargin}{0in} %{.4375in}

\setlength{\topmargin}{-.5in}  %{-.5625in}
\setlength{\footskip}{.25in} % to put page number 3/4" from the bottom of the page (1/4" from bottom of body text)
\setlength{\textheight}{9in}
\setlength{\textwidth}{6in}

%%% Alter LaTeX defaults to try to eliminate all widows and orphans
\clubpenalty=10000
\widowpenalty=10000

%%% try to avoid overfull lines by limiting how far it is okay to exceed the margins
%%% http://www.tex.ac.uk/cgi-bin/texfaq2html?label=overfull
\setlength{\emergencystretch}{2em}

\long\def\abstract#1{\gdef\@abstract{#1}}

\endinput
%% 
%% End of file `puthesis.cls'.

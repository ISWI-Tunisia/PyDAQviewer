doconce format html Tutorial --html_style=bootswatch_flatly --pygments_html_style=monokai --html_admon=bootstrap_panel --html_output=Tutorial --keep_pygments_html_bg --html_code_style=inherit --html_pre_style=inherit --html_links_in_new_window

doconce pygmentize Tutorial.do.txt perldoc

doconce format pdflatex Tutorial "--latex_code_style=default:pyg-blue1@dat:lst[style=gray]@sys:vrb[frame=lines,label=\\fbox{{\tiny Terminal}},framesep=2.5mm,framerule=0.7pt,fontsize=\fontsize{9pt}{9pt}]" --latex_code_bg_vpad

pdflatex -shell-escape Tutorial.tex
pdflatex -shell-escape Tutorial.tex

cp Tutorial.html Tutorial.pdf Tutorial.tex Tutorial.do.txt.html ../
cp -r imgs ../
doconce clean

#!/bin/bash
drive pull -y -explicitly-export -export docx -exports-dir ~/repos/ox-clo/lab-source/ -same-exports-dir ~/drive/ox-clo/docs/
drive pull -y -explicitly-export -export pdf -exports-dir ~/repos/ox-clo/lab-exercises/ -same-exports-dir ~/drive/ox-clo/docs/
drive pull -y -explicitly-export -export pptx -exports-dir ~/repos/ox-clo/pres-source/ -same-exports-dir ~/drive/ox-clo/slides/
drive pull -y -explicitly-export -export pdf -exports-dir ~/repos/ox-clo/presentations/ -same-exports-dir ~/drive/ox-clo/slides/
cd ~/repos/ox-clo
git add .
git commit -m "updated slides and docs"
git push

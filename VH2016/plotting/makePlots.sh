#for CHAN in eeet eemt eett eeem emmt mmmt mmtt emmm emt mmt ett mtt llet llmt llem lltt whlep whhad zh wh; do
#for CHAN in whlep whhad wh; do
#for CHAN in whlep whhad ; do
#for CHAN in zh; do
#    echo ${CHAN}
#    python plot_VH_postfit81X.py --fs ${CHAN} --fit "postfit" --unblind=1
#    #python plot_VH.py --fs ${CHAN} --fit "prefit" --unblind=1
#done

#for CHAN in zh wh; do
for CHAN in eeet eemt eett eeem emmt mmmt mmtt emmm emt mmt ett mtt llet llmt llem lltt whlep whhad zh wh; do
    echo ${CHAN}
    #python plot_VH_postfit81X.py --fs ${CHAN} --fit "postfit" --unblind=1 --ratio "alterRatio"
    python plot_VH_postfit81X_orig.py --fs ${CHAN} --fit "postfit" --unblind=1
    #python plot_VH.py --fs ${CHAN} --fit "prefit" --unblind=1
done

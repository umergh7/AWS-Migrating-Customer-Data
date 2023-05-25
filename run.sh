filenametime=$(date +"%m%d%Y%H%M%S")
#########################################################
# Part 2: SET VARIABLES 
export PYTHON_SCRIPT_NAME='run.py' # get the py_script from config.toml, and remove the quotes
export SCRIPTS_FOLDER=$(pwd)
export LOGDIR=$SCRIPTS_FOLDER/log
export LOG_FILE=${LOGDIR}/${SHELL_SCRIPT_NAME}_${filenametime}.log
#########################################################
# PART 3: GO TO SCRIPT FOLDER AND RUN
cd ${SCRIPTS_FOLDER}

#########################################################
# PART 4: SET LOG RULES

exec > >(tee ${LOG_FILE}) 2>&1

#########################################################
# PART 5: RUN SCRIPT
source sandbox/bin/activate

echo "Start to run Python Script"
python3 ${SCRIPTS_FOLDER}/${PYTHON_SCRIPT_NAME}


RC1=$?
if [ ${RC1} != 0 ]; then
	echo "PYTHON RUNNING FAILED"
	echo "[ERROR:] RETURN CODE:  ${RC1}"
	echo "[ERROR:] REFER TO THE LOG FOR THE REASON FOR THE FAILURE."
	exit 1
fi

echo "PROGRAM SUCCEEDED"

deactivate

exit 0 
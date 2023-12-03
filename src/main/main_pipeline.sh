#verifier que les variables d'environement sont bien definies
vars="username password mail matiere gitlabArbre repository_path"
for element in $vars
do
  if test "$(eval echo \$$element)" = ""; then
    echo "variable environmentale $element is not defined, exiting ..."
    exit 0
  fi
done


#creer variables.json à partir des variables d'environement 
envsubst < src/variables_template.json > src/variables.json

# vérifier si le pipeline est declenché par un trigger d'un depot etudiant
if test "$CI_PIPELINE_SOURCE" = "trigger"; then
    # Récupérer les informations sur le commit fait 
    curl --header "PRIVATE-TOKEN: $password" "https://gitlab.com/api/v4/projects/$PROJECT_SOURCE_ID/repository/commits/$COMMIT_SOURCE_SHA/diff" > response_diff.txt
    curl --header "PRIVATE-TOKEN: $password" "https://gitlab.com/api/v4/projects/$PROJECT_SOURCE_ID/repository/commits/$COMMIT_SOURCE_SHA" > response_project.txt

    #extraire l'url du projet d'etudiant
    project_source_url=$(cat response_project.txt | jq -r '.web_url')

    # Extraire la liste des fichiers modifiés
    modified_files=$(cat response_diff.txt | jq -r '.[].new_path')

    # extraire la description du commit
    cat response_project.txt | jq -r '.message' > commit_desc.txt

    # verifier que le commit n'est pas automatique, celui fait par la framework elle meme lors d'une evaluation d'avant
    if cat commit_desc.txt | grep -q 'automatique'; then
        echo "Le commit etait automatique abondan."
        exit 0 
    else
        # generer les arguments pour le script evaluateOnDemand 
        args_EOD=$(python3 src/utils/get_args_EOD.py $project_source_url $modified_files)
        echo "Lancer evaluateOnDemand $args_EOD"    
        # lancer evaluation
        sh feat3p evaluateOnDemand $args_EOD
    fi
# si le pipeline est lancé par le prof manuellement ou par un commit sur le projet Autotester2
else
    # recuperer la variable type_evaluate, et args
    if test "$type_evaluate" = "single"; then
        echo "lancer evaluate $args"
        # lancer le script evaluate 
        sh feat3p evaluate $args
    else
        if test "$type_evaluate" = "all"; then 
            echo "lancer evaluateAll $args"
            # lancer le script evaluateAll 
            sh feat3p evaluateAll $args
        else
            echo "varible type_evaluate not provided, exiting ..."
        fi
    fi
fi

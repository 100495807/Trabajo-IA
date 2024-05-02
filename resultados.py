from MFIS_Read_Functions import readFuzzySetsFile, readApplicationsFile, readRulesFile, readauxFile

fuzzy_sets = readFuzzySetsFile("inputvarsets.txt")
applications = readApplicationsFile()

with open("aux.txt", "w") as file:
    for app in applications:
        file.write(f"{app.appId}, ")
        for data_point in app.data:
            attribute_name = data_point[0]
            attribute_value = data_point[1]
            max_membership_degree = -1
            max_membership_label = None

            # Buscar el conjunto difuso correspondiente al atributo
            for key, fuzzy_set in fuzzy_sets.items():
                if attribute_name in key:
                    # Calcular el grado de membresía para el conjunto difuso
                    membership_degree = fuzzy_set.calculateMembershipDegree(attribute_value)
                    # Si el grado de membresía es mayor que el máximo actual, actualizar el máximo y la etiqueta
                    if membership_degree > max_membership_degree:
                        max_membership_degree = membership_degree
                        max_membership_label = fuzzy_set.label

            # Si se encontró un conjunto difuso con el máximo grado de membresía, escribir el nombre del atributo seguido de la etiqueta en el archivo
            if max_membership_label is not None:
                file.write(f"{attribute_name}, {max_membership_label}, ")
            else:
                file.write(f"No fuzzy set found for attribute: {attribute_name}, ")

        file.write("\n")

rules = readRulesFile()
aux = readauxFile()
for app in aux:
    print(f"App ID: {app.appId}")
    for data_point in app.data:
        print(f"Attribute: {data_point[0]}, Value: {data_point[1]}")
    print()  # Agrega una línea en blanco para separar cada aplicación

for rule in rules:
    print(f"Rule Name: {rule.ruleName}")
    print(f"Consequent: {rule.consequent}")
    for antecedent in rule.antecedent:
        print(f"Antecedent: {antecedent}")
    print()  # Agrega una línea en blanco para separar cada regla


def evaluate_applications(aux, rules):
    results = {}

    for application in aux:
        application_id = application.appId
        application_risk = None  # Inicializar el riesgo como None por defecto
        application_data_set = set(
            tuple(data) for data in application.data)  # Convertir los datos de la aplicación en un conjunto de tuplas

        for rule in rules:
            rule_antecedents = set(rule.antecedent)

            # Verificar si todos los antecedentes de la regla están contenidos en los datos de la aplicación
            if rule_antecedents.issubset(application_data_set):
                # Si los antecedentes coinciden, actualizar el riesgo
                if rule.consequent == "Risk=HighR":
                    application_risk = "HighR"
                elif rule.consequent == "Risk=MediumR" and application_risk != "HighR":
                    application_risk = "MediumR"
                elif rule.consequent == "Risk=LowR" and application_risk is None:
                    application_risk = "LowR"

        # Almacenar el riesgo de la aplicación en el diccionario de resultados
        results[application_id] = application_risk

    # Escribir los resultados en el archivo "results.txt"
    with open("results.txt", "w") as results_file:
        for app_id, risk in results.items():
            results_file.write(f"{app_id} {risk}\n")


evaluate_applications(aux, rules)
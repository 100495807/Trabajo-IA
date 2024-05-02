from MFIS_Read_Functions import readFuzzySetsFile, readApplicationsFile, readRulesFile, readauxFile
import numpy as np
import matplotlib.pyplot as plt


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
'''for app in aux:
    print(f"App ID: {app.appId}")
    for data_point in app.data:
        print(f"Attribute: {data_point[0]}, Value: {data_point[1]}")
    print()  # Agrega una línea en blanco para separar cada aplicación

for rule in rules:
    print(f"Rule Name: {rule.ruleName}")
    print(f"Consequent: {rule.consequent}")
    for antecedent in rule.antecedent:
        print(f"Antecedent: {antecedent}")
    print()  # Agrega una línea en blanco para separar cada regla'''


def evaluate_applications(applications, rules):
    # Diccionario para almacenar los resultados
    results = {}

    # Iterar sobre cada aplicación
    for application in applications:
        application_id = application.appId
        max_consequent_value = 0  # Valor máximo del consecuente encontrado
        max_consequent_label = None  # Etiqueta correspondiente al valor máximo

        # Iterar sobre cada regla
        for rule in rules:
            # Verificar si todos los antecedentes de la regla coinciden con los datos de la aplicación
            antecedents_matched = True
            for antecedent in rule.antecedent:
                antecedent_matched = False
                antecedent_name, antecedent_value = antecedent.split('=')
                for data_point in application.data:
                    if antecedent_name == data_point[0] and antecedent_value == data_point[1]:
                        antecedent_matched = True
                        break
                if not antecedent_matched:
                    antecedents_matched = False
                    break

            # Si todos los antecedentes coinciden, obtener el valor del consecuente
            if antecedents_matched:
                consequent_value = 0
                if rule.consequent == "Risk=HighR":
                    consequent_value = 3
                elif rule.consequent == "Risk=MediumR":
                    consequent_value = 2
                elif rule.consequent == "Risk=LowR":
                    consequent_value = 1

                # Actualizar el valor máximo si es necesario
                if consequent_value > max_consequent_value:
                    max_consequent_value = consequent_value
                    max_consequent_label = rule.consequent.split('=')[1]

        # Almacenar el valor máximo encontrado para la aplicación
        results[application_id] = max_consequent_value


    return results




# Escribir los resultados en el archivo "results.txt"
# Obtener los resultados
results = evaluate_applications(aux, rules)

# Escribir los resultados en el archivo "results.txt"
with open("results.txt", "w") as results_file:
    for app_id, risk_label in results.items():
        # Convertir el número en etiqueta correspondiente
        if risk_label == 3:
            risk = "HighR"
        elif risk_label == 2:
            risk = "MediumR"
        elif risk_label == 1:
            risk = "LowR"
        else:
            risk = "Unknown"

        results_file.write(f"{app_id} {risk}\n")


def plot_fuzzy_set(x, y, label):
    plt.plot(x, y, label=label)
def read_fuzzy_sets(file_name):
    fuzzy_sets = {}

    with open(file_name, "r") as file:
        for line in file:
            # Dividir la línea en partes
            parts = line.strip().split(',')

            # Obtener el nombre y la etiqueta del conjunto difuso
            variable, label = parts[0].split('=')

            # Obtener los puntos del conjunto difuso
            points = list(map(float, parts[3:]))

            # Si la variable no está en el diccionario, agregarla
            if variable not in fuzzy_sets:
                fuzzy_sets[variable] = {}

            # Agregar el conjunto difuso a la variable correspondiente en el diccionario
            fuzzy_sets[variable][label] = points

    return fuzzy_sets

# Leer los conjuntos difusos del archivo
fuzzy_sets = read_fuzzy_sets("inputvarsets.txt")

# Graficar cada conjunto borroso
for variable, labels in fuzzy_sets.items():
    plt.figure(figsize=(8, 5))
    plt.title(f'{variable} Fuzzy Sets')
    plt.xlabel(variable)
    plt.ylabel('Membership')
    for label, points in labels.items():
        x = np.linspace(points[0], points[-1], 100)
        y = np.interp(x, points, [0, 1, 1, 0])
        plot_fuzzy_set(x, y, label)
    plt.legend()
    plt.grid(True)
    plt.show()
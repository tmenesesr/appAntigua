import streamlit as st
import pandas as pd
import numpy as np

from scipy.interpolate import CubicSpline
from scipy.stats import norm
import random
import math

import altair as alt

import matplotlib.pyplot as plt
import seaborn as sns

from streamlit_metrics import metric, metric_row
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder

from PIL import Image

from fpdf import FPDF

st.set_page_config(layout="wide")


def main():
    pages = {
        "Home": page_home,
        "Flotation Model": page_model,
        "Sensitivity analysis": page_sensitivity,
        "Economic Evaluation": page_eco,
    }

    if "page" not in st.session_state:
        st.session_state.update(
            {
                # Default page
                "page": "Home",
                # Radio, selectbox and multiselect options
                "options": ["Hello", "Everyone", "Happy", "Streamlit-ing"],
                # Default widget values
                "text": "",
                "slider": 0,
                "checkbox": False,
                "radio": "Hello",
                "selectbox": "Hello",
                "multiselect": ["Hello", "Everyone"],
            }
        )

    with st.sidebar:
        page = st.radio("Go to", tuple(pages.keys()))
    pages[page]()


def page_home():
    col1111, col1112, col1113 = st.columns((1, 8, 1.5))
    with col1113:
        image = Image.open("FLS1.jpg")
        st.image(image, caption="OCS")
        st.write("")
    with col1112:
        st.title("Evaluation of Milling-Flotation Productivity Improvement Strategies")
    cola111, cola112, cola113 = st.columns((8, 1, 10))
    with cola111:
        st.write("")
        st.write("")
        st.write("")
        st.write(
            f"""
    Many available control strategies are associated with individual improvements for Flotation or Grinding, and very few address the interrelationship between Grinding and Flotation in search of a global optimum. A methodology is presented to evaluate different control strategies focused on reducing the dispersion of the degree of liberation that can cause significant recovery losses. The method relies on historical P80 measurements in the plant, generating a statistical model that represents the plant data. At the same time, it makes use of a P80 versus Laboratory recovery curve and the Monte Carlo method to evaluate the impact on the recovery of different P80 distributions generated by different control strategies.
    """
        )
    with cola113:
        st.write("")
        st.write("")
        st.write("")
        image = Image.open("image2_en.png")
        st.image(image)
        st.write("")


def page_model():
    col11, col12, col13 = st.columns((1, 8, 1.5))

    with col12:
        st.title("Evaluation of Milling-Flotation Productivity Improvement Strategies")
        st.write("")
    with col13:
        image = Image.open("FLS1.jpg")
        st.image(image, caption="OCS")
        st.write("")

    col111, col112, col113, col114, col115 = st.columns((1, 2, 2, 2, 1))
    with col113:
        global file_template
        file_template = st.file_uploader("Upload File")
        st.write("")
        st.write("")
        st.write("")

    col21, col22, col23 = st.columns((1, 1, 1))
    with col22:
        if file_template is not None:
            file_template.seek(0)
            df_upload = pd.read_csv(
                file_template,
                sep=";",
            )
            average_p80_val = int(df_upload.iloc[0]["Average_p80"])
            std_p80_val = int(df_upload.iloc[0]["Standard_deviation_p80"])
            simul_number_val = int(df_upload.iloc[0]["Number_simulations"])
            node_number_val = int(df_upload.iloc[0]["Number_nodes"])

        else:
            average_p80_val = 200
            std_p80_val = 15
            simul_number_val = 1000
            node_number_val = 3

        templates = ["1-Chuquicamata", "2-El Salvador", "3-Disputada", "4-Customizable"]
        st.subheader("Plant historical P80 data")
        st.write("")
        average_p80 = st.number_input(
            "Average P80", min_value=35, max_value=300, value=average_p80_val
        )
        std_p80 = st.number_input(
            "Standard Deviation P80", min_value=1, value=std_p80_val
        )
        st.session_state.simul_number = st.number_input(
            "Number of Simulations",
            min_value=1,
            value=simul_number_val,
        )
        node_number = st.number_input(
            "Number of Nodes", min_value=3, max_value=8, value=node_number_val
        )
        template_sim = st.selectbox("Select a Template", templates, index=3)
    st.write("")
    st.write("")

    node_max = node_number - 1
    middle_node_f = math.floor(node_max / 2)
    middle_node_c = math.ceil(node_max / 2)
    for i in range(node_number):
        j = i + 1
        if i < middle_node_f:
            globals()["val_rec_%s" % j] = round(
                85 * (1 - (middle_node_f - i) / node_max)
            )
        elif i == middle_node_f or i == middle_node_c:
            globals()["val_rec_%s" % j] = 85
        else:
            globals()["val_rec_%s" % j] = round(
                85 * (1 + (middle_node_f - i) / node_max)
            )

    for i in range(node_number):
        j = i + 1
        if i < middle_node_c:
            globals()["val_p80_%s" % j] = round(120 * (1 - (node_max - j) / node_max))
        elif i == middle_node_f:
            globals()["val_p80_%s" % j] = 120
        else:
            globals()["val_p80_%s" % j] = round(120 * (0.8 * (j) / middle_node_c))

    col31, col32, col33, col34, col35 = st.columns((1, 4, 2, 4, 1))

    # generamos 3 columnas
    with col34:
        if template_sim == templates[3]:
            st.subheader("Laboratory Recovery versus P80 Table")
    # generamos 3 columnas
    col41, col42, col43, col44 = st.columns((4, 1, 2, 2))

    with col43:
        st.write("")
        p80_list2 = []
        p80_list2.append(0)
        if file_template is not None:
            for i in range(node_number):
                j = i + 1
                a = st.number_input(
                    f"P80 {j}", max_value=300, value=int(df_upload.iloc[i]["p80"])
                )
                p80_list2.append(a)

        else:
            i = 0
            if template_sim == templates[3]:
                try:
                    for i in range(node_number):
                        j = i + 1
                        a = st.number_input(
                            f"P80 {j}", max_value=300, value=globals()["val_p80_%s" % j]
                        )
                        p80_list2.append(a)

                except:
                    st.error("Valor de p80 debe ser menor al siguiente")
                    st.stop()
            else:
                chuqui = {
                    "p80": [20, 50, 100, 150, 185, 200, 230],
                    "Recovery": [30, 66, 90, 90, 76, 66, 35],
                }
                df_chuqui = pd.DataFrame(chuqui)
                salvador = {"p80": [20, 65, 110, 150], "Recovery": [50, 81, 80, 52]}
                df_salvador = pd.DataFrame(salvador)
                disputada = {
                    "p80": [10, 50, 65, 80, 150, 180],
                    "Recovery": [51, 82, 89, 91, 75, 52],
                }
                df_disputada = pd.DataFrame(disputada)
                if template_sim == templates[0]:
                    df_template = df_chuqui
                elif template_sim == templates[1]:
                    df_template = df_salvador
                elif template_sim == templates[2]:
                    df_template = df_disputada
                p80_list2 = list(df_template["p80"])
        contador = 0
        if template_sim == templates[3]:
            for i in range(node_number):
                if i > 1:
                    j = i - 1
                    if p80_list2[i] > p80_list2[j]:
                        contador += 1
        else:
            contador = node_number - 2

    if contador == node_number - 2:
        with col32:
            st.subheader("Recovery versus P80 Graph")
            rec_list = []
            rec_list.append(0)
        with col44:
            st.write("")
            if file_template is not None:
                for i in range(node_number):
                    j = i + 1
                    b = st.number_input(
                        f"Recovery {j}",
                        min_value=0,
                        max_value=100,
                        value=int(df_upload.iloc[i]["Recovery"]),
                    )
                    rec_list.append(b)

            else:
                i = 0
                if template_sim == templates[3]:
                    for i in range(node_number):
                        j = i + 1
                        b = st.number_input(
                            f"Recovery {j}",
                            min_value=0,
                            max_value=100,
                            value=globals()["val_rec_%s" % j],
                        )
                        rec_list.append(b)
                else:
                    rec_list = list(df_template["Recovery"])

        data = []
        if template_sim == templates[3]:
            for i in range(node_number):
                j = i + 1
                data.append([p80_list2[j], rec_list[j]])

            df_test = pd.DataFrame(data, columns=("p80", "Recovery"))
        else:
            df_test = df_template.copy()

        st.session_state.x = df_test["p80"]
        st.session_state.y = df_test["Recovery"]

        p80_min = df_test["p80"].min()
        p80_max = df_test["p80"].max()

        max_graph = round(p80_max * 1.1)
        min_graph = round(p80_min * 0.8)

        f = CubicSpline(st.session_state.x, st.session_state.y, bc_type="natural")
        st.session_state.f = f

        st.session_state.x1_min = df_test["p80"].iloc[0]
        slope_1 = f(st.session_state.x1_min, 1)
        c_1 = df_test["Recovery"].iloc[0] - slope_1 * st.session_state.x1_min
        x0_1 = -c_1 / slope_1
        st.session_state.x_new_1 = np.linspace(0, st.session_state.x1_min - 1, 100)
        st.session_state.y_new_1 = st.session_state.x_new_1 * slope_1 + c_1

        st.session_state.x2_max = df_test["p80"].iloc[-1]
        slope_2 = f(st.session_state.x2_max, 1)
        c_2 = df_test["Recovery"].iloc[-1] - slope_2 * st.session_state.x2_max
        st.session_state.x0_2 = -c_2 / slope_2
        st.session_state.x_new_2 = np.linspace(
            st.session_state.x2_max + 1, st.session_state.x0_2, 100
        )
        st.session_state.y_new_2 = st.session_state.x_new_2 * slope_2 + c_2

        prob = random.random()
        norm.ppf(prob, loc=average_p80, scale=std_p80)
        df_rand = pd.DataFrame(
            np.random.random(size=(st.session_state.simul_number, 1)),
            columns=["random"],
        )
        df_rand["Simulated_p80"] = norm.ppf(
            df_rand["random"], loc=average_p80, scale=std_p80
        )

        def check(row):
            if row["Simulated_p80"] < 35:
                val = np.nan
            elif row["Simulated_p80"] > st.session_state.x0_2:
                val = np.nan
            else:
                val = row["Simulated_p80"]
            return val

        df_rand["Simulated_p80_check"] = df_rand.apply(check, axis=1)
        df_rand["recovery"] = df_rand["Simulated_p80_check"].apply(f)

        st.session_state.simul_recovery = df_rand[df_rand["recovery"] > 0][
            "recovery"
        ].mean()
        st.session_state.simul_recovery = round(st.session_state.simul_recovery, 2)

        st.session_state.df_rand = df_rand

        with col41:
            st.subheader("")
            color1 = "#002A54"
            #'midnightblue'
            color2 = "#C94F7E"
            #'purple'
            plt.style.use("default")
            x_new = np.linspace(st.session_state.x1_min, st.session_state.x2_max, 100)
            y_new = f(x_new)
            plt.rcParams.update({"font.size": 16})
            fig1, ax = plt.subplots(figsize=(12, 8))
            ax2 = ax.twinx()
            plt.grid(True, axis="y", linewidth=0.2, color="gray", linestyle="-")
            ax.fill_between(x_new, y_new, alpha=0.1, color=color1, linewidth=2)
            ax.fill_between(
                st.session_state.x_new_1,
                st.session_state.y_new_1,
                alpha=0.1,
                color=color1,
                linewidth=2,
            )
            ax.fill_between(
                st.session_state.x_new_2,
                st.session_state.y_new_2,
                alpha=0.1,
                color=color1,
                linewidth=2,
            )
            ax.plot(x_new, y_new, linewidth=2, color=color1, alpha=0.8)
            ax.plot(st.session_state.x, st.session_state.y, "o", color=color1)
            ax.set_ylabel("Recovery", color=color1)
            ax.set_xlabel("P80")
            # plt.axhline(y = thr_mean, color = 'r', linestyle = '--',linewidth =0.4)
            # fig1.text(0.7,0.4,'Average: '+str(round(thr_mean)),color='red',size=4)
            plt.ylabel("", fontsize=16)
            plt.xlabel("", fontsize=16)
            ax.tick_params(axis="both", which="major", labelsize=16, width=0.2)
            ax.spines["top"].set_linewidth("0.3")
            ax.spines["right"].set_linewidth("0.3")
            ax.spines["bottom"].set_linewidth("0.3")
            ax.spines["left"].set_linewidth("0.3")
            ax.set_ylim([0, 100])
            ax.plot(
                st.session_state.x_new_1,
                st.session_state.y_new_1,
                color=color1,
                linewidth=2,
            )

            ax.plot(
                st.session_state.x_new_2,
                st.session_state.y_new_2,
                color=color1,
                linewidth=2,
            )

            ax2 = sns.histplot(
                df_rand,
                x="Simulated_p80_check",
                bins=20,
                color=color2,
            )

            ## ESTE ES EL PEDAZO INSERTADO
            # Create a figure and an axis
            fig1, ax = plt.subplots(figsize=(12, 8))

            # Add a line to the axis
            ax.plot([1, 2, 3], [4, 5, 6])
            ## ESTE ES EL PEDAZO INSERTADO

            ax2.set_ylabel("Count", color=color2)

            # plt.title('Curva Recuperación versus P80',fontsize=22)
            st.pyplot(fig1)
            st.write("pasó por la 399")

            metric(
                "Simulated Recovery",
                st.session_state.simul_recovery,
            )

        def convert_df(df):
            return df.to_csv(sep=";", index=False).encode("latin-1")

        with col43:
            st.write("")
            st.write("")
            column_names = [
                "Average_p80",
                "Standard_deviation_p80",
                "Number_simulations",
                "Number_nodes",
                "p80",
                "Recovery",
            ]
            if template_sim == templates[3]:
                df_donwload = df_test.copy()
                listofzeros_av = [""] * (node_number - 1)
                listofzeros_av.insert(0, average_p80)
                listofzeros_st = [""] * (node_number - 1)
                listofzeros_st.insert(0, std_p80)
                listofzeros_sim = [""] * (node_number - 1)
                listofzeros_sim.insert(0, st.session_state.simul_number)
                listofzeros_nod = [""] * (node_number - 1)
                listofzeros_nod.insert(0, node_number)
                df_donwload.insert(loc=0, column="Number_nodes", value=listofzeros_nod)
                df_donwload.insert(
                    loc=0, column="Number_simulations", value=listofzeros_sim
                )
                df_donwload.insert(
                    loc=0, column="Standard_deviation_p80", value=listofzeros_st
                )
                df_donwload.insert(loc=0, column="Average_p80", value=listofzeros_av)

                csv = convert_df(df_donwload)
                file_download = st.download_button(
                    "Template File", data=csv, file_name="template.csv"
                )

        with col41:
            import base64

            def create_download_link(val, filename):
                b64 = base64.b64encode(val)  # val looks like b'...'
                return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

            export_as_pdf = st.button("Export Report")
            if export_as_pdf:
                pdf = FPDF(orientation="P", unit="mm", format="A4")
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.image("FLS1.jpg", x=180, y=0, w=30, h=30)
                title = "Evaluation of Milling-Flotation Productivity Improvement Strategies"
                intro = "    Many available control strategies are associated with individual improvements for Flotation or Grinding, and very few address the interrelationship between Grinding and Flotation in search of a global optimum. A methodology is presented to evaluate different control strategies focused on reducing the dispersion of the degree of liberation that can cause significant recovery losses. The method relies on historical P80 measurements in the plant, generating a statistical model that represents the plant data. At the same time, it makes use of a P80 versus Laboratory recovery curve and the Monte Carlo method to evaluate the impact on the recovery of different P80 distributions generated by different control strategies.    "
                pdf.multi_cell(w=150, h=7, txt=title, border=0, align="J", fill="False")
                # pdf.cell(40, 10, title)
                pdf.set_font("Arial", "", 12)
                pdf.ln(h="")
                pdf.ln(h="")
                pdf.ln(h="")
                pdf.ln(h="")
                # pdf.cell(60,23, intro,0, 1, 'C')
                pdf.multi_cell(w=0, h=8, txt=intro, border=1, align="J", fill="False")
                # ,str = 'J',bool = False)
                # pdf.text(2, 25,intro)
                fig1.savefig("fig1.jpg")
                pdf.image("image2_en.png", x=50, y=140, w=130, h=90)
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.image("FLS1.jpg", x=180, y=0, w=30, h=30)
                pdf.multi_cell(w=150, h=7, txt=title, border=0, align="J", fill="False")
                pdf.set_font("Arial", "", 12)
                pdf.text(20, 40, f"Parameters")
                pdf.text(50, 50, f"Average P80: {str(average_p80)}")
                pdf.text(50, 60, f"Standard Deviation P80: {str(std_p80)}")
                pdf.text(50, 80, f"Number of Nodes: {str(node_number)}")
                pdf.text(
                    50,
                    70,
                    f"Number of Simulations: {str( st.session_state.simul_number)}",
                )
                pdf.text(20, 95, f"Laboratory Recovery versus P80 Table")
                pdf.set_font("Arial", "", 10)
                for i in range(node_number):
                    j = i + 1
                    pdf.text(
                        50,
                        100 + j * 7,
                        f"P80 {j}: {str(p80_list2[j])}  |  Recovery {j}: {rec_list[j]}",
                    )

                pdf.image("fig1.jpg", x=40, y=160, w=130, h=90)
                pdf.set_font("Arial", "b", 16)
                pdf.text(
                    60,
                    260,
                    f"Simulated Recovery: {str(st.session_state.simul_recovery)}",
                )

                html = create_download_link(
                    pdf.output(dest="S").encode("latin-1"), "Report_P80"
                )

                st.markdown(html, unsafe_allow_html=True)

    else:
        with col41:
            st.write("")
            st.subheader("Los valores de P80 deben ser estrictamente crecientes")
            #    st.write('')
            #   st.write('')


def page_sensitivity():
    col11, col12, col13 = st.columns((1, 8, 1.5))

    with col12:
        st.title("Evaluation of Milling-Flotation Productivity Improvement Strategies")
        st.write("")
    with col13:
        image = Image.open("FLS1.jpg")
        st.image(image, caption="OCS")
        st.write("")

    st.subheader("Sensitivity Analysis")
    st.write("")
    col111, col112, col113, col114, col115 = st.columns((2, 3, 2, 3, 2))

    with col112:
        mean_p80_min = st.number_input(
            "Minimun value of mean P80", min_value=35, max_value=300, value=100
        )
        mean_p80_max = st.number_input(
            "Maximum value of mean P80", min_value=35, max_value=300, value=250
        )
    with col114:
        std_p80_min = st.number_input(
            "Minimum Standar deviation", min_value=0, max_value=300
        )
        std_p80_max = st.number_input(
            "Maximum Standar deviation", min_value=0, max_value=300, value=30
        )

    st.write("")
    st.write("")
    st.write("")

    col211, col212, col213, col214, col215 = st.columns((1, 12, 1, 5, 1))

    def check(row):
        if row["Simulated_p80"] < 35:
            val = np.nan
        elif row["Simulated_p80"] > 350:
            val = np.nan
        else:
            val = row["Simulated_p80"]
        return val

    with col212:
        st.subheader("Recovery versus P80 Standar Deviation Graph")
        simul_number1 = st.session_state.simul_number

        list_rec = []
        list_std = []
        list_mean = []
        number_sim = 20
        for j in range(1, 5):
            average_p80 = mean_p80_min + (mean_p80_max - mean_p80_min) * (j - 1) / 3
            list_mean.append(round(average_p80))
            for i in range(0, number_sim):
                std_aux = std_p80_min + (std_p80_max - std_p80_min) * i / (
                    number_sim - 1
                )
                prob = random.random()
                df_rand = pd.DataFrame(
                    np.random.random(size=(simul_number1, 1)), columns=["random"]
                )
                df_rand["Simulated_p80"] = norm.ppf(
                    df_rand["random"], loc=average_p80, scale=std_aux
                )
                df_rand["Simulated_p80_check"] = df_rand.apply(check, axis=1)
                df_rand["recovery"] = df_rand["Simulated_p80_check"].apply(
                    st.session_state.f
                )
                simul_recovery_aux = df_rand[df_rand["recovery"] > 0]["recovery"].mean()
                simul_recovery_aux = round(simul_recovery_aux, 2)
                list_rec.append(simul_recovery_aux)
                list_std.append(std_aux)
        list_mean2 = [str(i) for i in list_mean]
        mystring = "P80 mean : "
        list_mean3 = [mystring + s for s in list_mean2]
        fig2, ax = plt.subplots(figsize=(12, 8))
        # plt.style.use('bmh')
        plt.grid(True, axis="y", linewidth=0.2, color="gray", linestyle="-")
        for i in range(4):
            # plt.style.use('bmh')
            ax.plot(
                list_std[i * number_sim : i * number_sim + number_sim],
                list_rec[i * number_sim : i * number_sim + number_sim],
                linewidth=2,
                alpha=0.8,
                label=list_mean3[i],
            )
            ax.legend()
        # color=color1,
        # ax.plot(x, y, 'o', color=color1)
        ax.set_ylabel("Recovery")
        ax.set_xlabel("P80 Standar Deviation")
        st.pyplot(fig2)
        # plt.plot(list_std,list_rec)


def page_eco():
    simul_number2 = 1000

    col11, col12, col13 = st.columns((1, 8, 1.5))

    with col12:
        st.title("Economic Evaluation")
        # st.write("")
    with col13:
        image = Image.open("FLS1.jpg")
        st.image(image, caption="OCS")
        st.write("")

    cola1, cola2, cola3 = st.columns((1, 8, 1))
    with cola2:
        average_p80 = st.number_input(
            "Average P80", min_value=35, max_value=300, value=180
        )
        std_p80_1 = st.number_input("Standard Deviation P80 - 1", min_value=1, value=35)
        std_p80_2 = st.number_input("Standard Deviation P80 - 2", min_value=1, value=15)
        ton_diario = st.number_input("Daily TPH", value=180000)
        ley = st.number_input("Average Copper Grade (Percentage)", value=0.9)
        precio = st.number_input("Copper Price (US$/lb)", value=4.86)
    st.write("")
    col21, col22, col23 = st.columns((8, 2, 8))
    with col21:
        st.subheader("")

        prob = random.random()
        norm.ppf(prob, loc=average_p80, scale=std_p80_1)
        df_rand = pd.DataFrame(
            np.random.random(size=(simul_number2, 1)), columns=["random"]
        )
        df_rand["Simulated_p80"] = norm.ppf(
            df_rand["random"], loc=average_p80, scale=std_p80_1
        )

        def check(row):
            if row["Simulated_p80"] < 35:
                val = np.nan
            elif row["Simulated_p80"] > st.session_state.x0_2:
                val = np.nan
            else:
                val = row["Simulated_p80"]
            return val

        df_rand["Simulated_p80_check"] = df_rand.apply(check, axis=1)
        df_rand["recovery"] = df_rand["Simulated_p80_check"].apply(st.session_state.f)

        st.session_state.simul_recovery = df_rand[df_rand["recovery"] > 0][
            "recovery"
        ].mean()
        st.session_state.simul_recovery = round(st.session_state.simul_recovery, 2)

        st.session_state.df_rand = df_rand

        color1 = "#002A54"
        #'midnightblue'
        color2 = "#C94F7E"
        #'purple'
        plt.style.use("default")
        x_new = np.linspace(st.session_state.x1_min, st.session_state.x2_max, 100)
        y_new = st.session_state.f(x_new)
        plt.rcParams.update({"font.size": 16})
        fig1, ax = plt.subplots(figsize=(12, 8))
        ax2 = ax.twinx()
        plt.grid(True, axis="y", linewidth=0.2, color="gray", linestyle="-")
        ax.fill_between(x_new, y_new, alpha=0.1, color=color1, linewidth=2)
        ax.fill_between(
            st.session_state.x_new_1,
            st.session_state.y_new_1,
            alpha=0.1,
            color=color1,
            linewidth=2,
        )
        ax.fill_between(
            st.session_state.x_new_2,
            st.session_state.y_new_2,
            alpha=0.1,
            color=color1,
            linewidth=2,
        )
        ax.plot(x_new, y_new, linewidth=2, color=color1, alpha=0.8)
        ax.plot(st.session_state.x, st.session_state.y, "o", color=color1)
        ax.set_ylabel("Recovery", color=color1)
        ax.set_xlabel("P80")
        # plt.axhline(y = thr_mean, color = 'r', linestyle = '--',linewidth =0.4)
        # fig1.text(0.7,0.4,'Average: '+str(round(thr_mean)),color='red',size=4)
        plt.ylabel("", fontsize=16)
        plt.xlabel("", fontsize=16)
        ax.tick_params(axis="both", which="major", labelsize=16, width=0.2)
        ax.spines["top"].set_linewidth("0.3")
        ax.spines["right"].set_linewidth("0.3")
        ax.spines["bottom"].set_linewidth("0.3")
        ax.spines["left"].set_linewidth("0.3")
        ax.set_ylim([0, 100])
        ax.plot(
            st.session_state.x_new_1,
            st.session_state.y_new_1,
            color=color1,
            linewidth=2,
        )
        ax.plot(
            st.session_state.x_new_2,
            st.session_state.y_new_2,
            color=color1,
            linewidth=2,
        )
        ax2 = sns.histplot(
            st.session_state.df_rand,
            x="Simulated_p80_check",
            bins=20,
            color=color2,
        )
        ax2.set_ylabel("Count", color=color2)
        ax.text(ax.get_xlim()[1] * 0.8, 90, f"std 1: {std_p80_1}")

        # plt.title('Curva Recuperación versus P80',fontsize=22)

        ## ESTE ES EL PEDAZO INSERTADO
        # Create a figure and an axis
        fig1, ax = plt.subplots(figsize=(12, 8))

        # Add a line to the axis
        ax.plot([1, 2, 3], [4, 5, 6])
        ## ESTE ES EL PEDAZO INSERTADO

        st.pyplot(fig1)

        metric(
            "Simulated Recovery",
            st.session_state.simul_recovery,
        )

    with col23:
        st.subheader("")

        prob = random.random()
        norm.ppf(prob, loc=average_p80, scale=std_p80_2)
        df_rand = pd.DataFrame(
            np.random.random(size=(simul_number2, 1)), columns=["random"]
        )
        df_rand["Simulated_p80"] = norm.ppf(
            df_rand["random"], loc=average_p80, scale=std_p80_2
        )

        def check(row):
            if row["Simulated_p80"] < 35:
                val = np.nan
            elif row["Simulated_p80"] > st.session_state.x0_2:
                val = np.nan
            else:
                val = row["Simulated_p80"]
            return val

        df_rand["Simulated_p80_check"] = df_rand.apply(check, axis=1)
        df_rand["recovery"] = df_rand["Simulated_p80_check"].apply(st.session_state.f)

        st.session_state.simul_recovery2 = df_rand[df_rand["recovery"] > 0][
            "recovery"
        ].mean()
        st.session_state.simul_recovery2 = round(st.session_state.simul_recovery2, 2)

        max_p80 = df_rand["Simulated_p80_check"].max()

        st.session_state.df_rand = df_rand

        color1 = "#002A54"
        #'midnightblue'
        color2 = "#C94F7E"
        #'purple'
        plt.style.use("default")
        x_new = np.linspace(st.session_state.x1_min, st.session_state.x2_max, 100)
        y_new = st.session_state.f(x_new)
        plt.rcParams.update({"font.size": 16})
        fig1, ax = plt.subplots(figsize=(12, 8))
        ax2 = ax.twinx()
        plt.grid(True, axis="y", linewidth=0.2, color="gray", linestyle="-")
        ax.fill_between(x_new, y_new, alpha=0.1, color=color1, linewidth=2)
        ax.fill_between(
            st.session_state.x_new_1,
            st.session_state.y_new_1,
            alpha=0.1,
            color=color1,
            linewidth=2,
        )
        ax.fill_between(
            st.session_state.x_new_2,
            st.session_state.y_new_2,
            alpha=0.1,
            color=color1,
            linewidth=2,
        )
        ax.plot(x_new, y_new, linewidth=2, color=color1, alpha=0.8)
        ax.plot(st.session_state.x, st.session_state.y, "o", color=color1)
        ax.set_ylabel("Recovery", color=color1)
        ax.set_xlabel("P80")
        # plt.axhline(y = thr_mean, color = 'r', linestyle = '--',linewidth =0.4)
        # fig1.text(0.7,0.4,'Average: '+str(round(thr_mean)),color='red',size=4)
        plt.ylabel("", fontsize=16)
        plt.xlabel("", fontsize=16)
        ax.tick_params(axis="both", which="major", labelsize=16, width=0.2)
        ax.spines["top"].set_linewidth("0.3")
        ax.spines["right"].set_linewidth("0.3")
        ax.spines["bottom"].set_linewidth("0.3")
        ax.spines["left"].set_linewidth("0.3")
        ax.set_ylim([0, 100])
        ax.plot(
            st.session_state.x_new_1,
            st.session_state.y_new_1,
            color=color1,
            linewidth=2,
        )
        ax.plot(
            st.session_state.x_new_2,
            st.session_state.y_new_2,
            color=color1,
            linewidth=2,
        )
        ax2 = sns.histplot(
            st.session_state.df_rand,
            x="Simulated_p80_check",
            bins=20,
            color=color2,
        )
        ax2.set_ylabel("Count", color=color2)
        ax.text(ax.get_xlim()[1] * 0.8, 90, f"std 2: {std_p80_2}")
        # plt.title('Curva Recuperación versus P80',fontsize=22)

        ## ESTE ES EL PEDAZO INSERTADO
        # Create a figure and an axis
        fig1, ax = plt.subplots(figsize=(12, 8))

        # Add a line to the axis
        ax.plot([1, 2, 3], [4, 5, 6])
        ## ESTE ES EL PEDAZO INSERTADO

        st.pyplot(fig1)
        # st.write(ax.get_xlim()[1])

        metric(
            "Simulated Recovery",
            st.session_state.simul_recovery2,
        )

    col31, col32, col33 = st.columns((2, 8, 2))
    rec_dif = st.session_state.simul_recovery2 - st.session_state.simul_recovery
    cobre_ad = ton_diario * ley / 100 * rec_dif / 100
    ppd = cobre_ad * 2204.63
    us_day = ppd * precio
    us_year = us_day * 365

    with col32:
        st.info(f"Recovery Difference: {round(rec_dif,2)}%")
        st.info(f"Daily Tons of Additional Fine Copper: {round(cobre_ad,2)} tpd")
        st.info(f"Pounds per day: {round(ppd,),:}")
        if us_day > 0:
            st.success(f"Additional Daily Income: {round(us_day,):,} US$/day")
            st.success(f"Additional Yearly Income: {round(us_year,):,} US$/year")
        else:
            st.error(f"Additional Daily Income: {round(us_day,):,} US$/day")
            st.error(f"Additional Yearly Income: {round(us_year,):,} US$/year")


if __name__ == "__main__":
    main()

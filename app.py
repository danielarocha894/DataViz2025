import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import streamlit.components.v1 as components  

# Configuração visual
df_rasse = pd.read_csv("20170308hundehalter.csv", encoding="latin1", sep=",")
df_rasse2 = pd.read_csv("zuordnungstabellehunderassehundetyp.csv", encoding="latin1", sep=";")

df = df_rasse.merge(df_rasse2.rename(columns={"dogbreedtype": "Breed_Type"}), how="left", left_on="BREED1", right_on="dogbreed")
df["DOG_AGE"] = 2025 - df["DOG_YEAR_OF_BIRTH"]

# Verificação
if "Breed_Type" not in df.columns:
    st.error("Erro: a coluna 'Breed_Type' não foi encontrada após o merge.")
    st.stop()

# Funções para cada gráfico
def grafico1():
    top_breeds = df["BREED1"].value_counts().head(10)
    breed_names = top_breeds.index
    breed_counts = top_breeds.values

    fig, ax = plt.subplots(figsize=(7, 4.5))
    bar_height = 0.6
    for i, (name, count) in enumerate(zip(breed_names, breed_counts)):
        y = i
        bar = FancyBboxPatch(
            (0, y - bar_height/2), count, bar_height,
            boxstyle="round,pad=0.05,rounding_size=6",
            ec="none",
            fc=sns.color_palette("pastel")[i % 10]
        )
        ax.add_patch(bar)
        ax.text(count + 5, y, f"{count}", va='center', fontsize=10)

    ax.set_yticks(range(len(breed_names)))
    ax.set_yticklabels(breed_names, fontsize=11)
    ax.set_title("Top 10 Dog Breeds")
    ax.set_xlim(0, max(breed_counts) * 1.1)
    ax.invert_yaxis()
    sns.despine(left=True, bottom=True)
    st.pyplot(fig)

def grafico2():
    counts = df["Breed_Type"].value_counts()
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        counts,
        labels=counts.index,
        autopct='%1.2f%%',
        startangle=90,
        colors=["#e64980", "#BCE5FF"],
        textprops={'fontsize': 10},
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
    )
    ax.add_artist(plt.Circle((0, 0), 0.93, color='white'))
    ax.set_title("Distribution by Breed Type")
    
    st.markdown("""
        <div style='margin-top: 15px;'>
        <p style='font-size: 15px;'><strong>Breed Type Legend:</strong></p>
        <ul style='font-size: 15px; line-height: 1.6; padding-left: 20px;'>
            <li><strong>"K" – Kleinwüchsig:</strong> Indicates small-sized breeds.</li>
            <li><strong>"I" – Rassentypenliste I:</strong> Breeds listed under Category I, often considered potentially dangerous under German regulations.</li>
            <li><strong>"II" – Rassentypenliste II:</strong> Breeds in Category II, typically subject to fewer restrictions.</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

    ax.axis("equal")
    st.pyplot(fig)


def grafico3():
    import matplotlib.patches as patches

    # Faixas etárias válidas esperadas
    valid_ranges = ["18-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81-90", "91-100"]
    df_age = df[df["AGE"].astype(str).isin(valid_ranges)]

    # Agrupar e ordenar
    grouped_age = df_age["AGE"].value_counts().reindex(valid_ranges).fillna(0)

    # Plot manual com FancyBboxPatch
    fig, ax = plt.subplots(figsize=(8, 5))
    bar_width = 0.8
    spacing = 1.2
    colors = sns.color_palette("pastel")

    for i, (age_range, count) in enumerate(grouped_age.items()):
        x = i * spacing
        bar = patches.FancyBboxPatch(
            (x, 0), bar_width, count,
            boxstyle="round,pad=0.02,rounding_size=4",
            ec="none",
            fc=colors[i % len(colors)]
        )
        ax.add_patch(bar)
        ax.text(x + bar_width / 2, count + 20, str(int(count)), ha='center', va='bottom', fontsize=9)

    # Eixos e ajustes
    ax.set_xlim(-0.5, len(valid_ranges) * spacing - 0.5)
    ax.set_ylim(0, grouped_age.max() * 1.2)
    ax.set_xticks([i * spacing + bar_width / 2 for i in range(len(valid_ranges))])
    ax.set_xticklabels(valid_ranges, rotation=45, fontsize=10)
    ax.set_ylabel("Number of Owners")
    ax.set_title("Owner Age Distribution")
    sns.despine(left=True, bottom=True)
    st.pyplot(fig)



def grafico4():
    dist = df["DOG_GENDER"].value_counts()
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        dist,
        labels=dist.index,
        autopct='%1.2f%%',
        startangle=90,
        colors=["#e64980", "#BCE5FF"],
        textprops={'fontsize': 10},
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
    )
    ax.add_artist(plt.Circle((0, 0), 0.93, color='white'))  # Donut
    ax.set_title("Dog Gender Distribution")
    ax.axis("equal")
    st.pyplot(fig)


def grafico5():
    counts = df["DOG_COLOR"].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=counts.values, y=counts.index, ax=ax, palette="flare")
    ax.set_title("Top 10 Dog Colors")
    st.pyplot(fig)

def grafico6():
    breed_gender_crosstab = pd.crosstab(df["Breed"], df["GENDER"])
    display(breed_gender_crosstab.head())

    # Optional: Plot top breeds by gender
    top_breed_names = top_breeds.index.tolist()
    subset = df[df["Breed"].isin(top_breed_names)]
    crosstab_top = pd.crosstab(subset["Breed"], subset["GENDER"])
    crosstab_top.plot(kind="bar", stacked=True)
    plt.title("Top Breeds by Owner Gender")
    plt.xlabel("Breed")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def grafico7():
    birth = df["DOG_YEAR_OF_BIRTH"].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.plot(birth.index, birth.values, marker="o", color="orange")
    ax.set_title("Dog Birth Year Distribution")
    st.pyplot(fig)

def grafico8():
    import matplotlib.patches as patches
    grouped = df.groupby(["Breed_Type", "GENDER"]).size().unstack(fill_value=0)
    labels = grouped.index.tolist()
    genders = grouped.columns.tolist()

    fig, ax = plt.subplots(figsize=(10, 5))
    spacing = 1.5
    bar_width = 0.35
    colors = sns.color_palette("pastel")

    for i, breed in enumerate(labels):
        x_base = i * spacing
        for j, gender in enumerate(genders):
            count = grouped.loc[breed, gender]
            x = x_base + j * bar_width
            bar = patches.FancyBboxPatch(
                (x, 0), bar_width, count,
                boxstyle="round,pad=0.02,rounding_size=4",
                ec="none",
                fc=colors[j % len(colors)]
            )
            ax.add_patch(bar)
            ax.text(x + bar_width / 2, count + 10, str(int(count)), ha='center', va='bottom', fontsize=8)

    ax.set_xlim(-0.5, len(labels) * spacing)
    ax.set_ylim(0, grouped.values.max() * 1.2)
    ax.set_xticks([i * spacing + bar_width for i in range(len(labels))])
    ax.set_xticklabels(labels, rotation=45, fontsize=9)
    ax.set_title("Breed Type by Owner Gender")
    st.markdown(""" <p style='font-size: 15px;'><strong>The dataset contains the following columns:</strong></p>
                        <ul style='font-size: 15px; line-height: 1.6; padding-left: 20px;'>
                            <li><strong>"K" – Kleinwüchsig: </strong>:indicates small-sized breeds.</li>
                            <li><strong>"I" – Rassentypenliste I:</strong>: refers to breeds listed under Category I, often associated with potentially dangerous breeds according to specific regulations in Germany.</li>
                            <li><strong>"II" – Rassentypenliste II:</strong>: refers to breeds listed under Category II, typically subject to less severe restrictions or legal requirements than those in Category I.</li>
                        </ul>
                    </p> 
                """)
    ax.set_ylabel("Count")
    ax.legend(genders, title="Gender")
    sns.despine(left=True, bottom=True)
    st.pyplot(fig)


def grafico9():
    valid_ages = {
        "18-20": 19, "21-30": 25, "31-40": 35, "41-50": 45,
        "51-60": 55, "61-70": 65, "71-80": 75, "81-90": 85, "91-100": 95
    }
    df_temp = df[df["AGE"].isin(valid_ages.keys())].copy()
    df_temp["AGE_NUM"] = df_temp["AGE"].map(valid_ages)
    fig, ax = plt.subplots()
    sns.boxplot(x="Breed_Type", y="AGE_NUM", data=df_temp, ax=ax)
    ax.set_title("Owner Age by Breed Type")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def grafico10():
    dogs_per_owner = df.groupby("OWNER_ID").size()
    display(dogs_per_owner.describe())

    sns.histplot(dogs_per_owner, bins=5)
    plt.title("Number of Dogs per Owner")
    plt.xlabel("Dogs Owned")
    plt.ylabel("Number of Owners")
    plt.tight_layout()
    plt.show()

# Títulos para menu
graficos = {
    "Top 10 Dog Breeds": grafico1,
    "Distribution by Breed Type": grafico2,
    "Owner Age Distribution": grafico3,
    "Dog Gender Distribution": grafico4,
    "Top 10 Dog Colors": grafico5,
    "Dogs per City District": grafico6,
    "Dog Birth Year Distribution": grafico7,
    "Breed Type by Owner Gender": grafico8,
    "Owner Age by Breed Type": grafico9,
    "Pure vs Mixed Breeds": grafico10,
}

st.title("🐶 Dog Data Explorer")
st.markdown("""
            *For this semester’s visualization project, our professor gave us the opportunity to choose any topic we liked. In this context, I decided to focus on something that represents both my greatest love and one of the things I miss the most: my dogs! Today, I would like to share some statistics showing how having a pet can be wonderful 
            not only for mental health but also for physical well-being.Professor Dina Deifallah, thank you very much for the opportunity to apply the knowledge from this semester while speaking about something I truly love.*  
            
            &nbsp;  
            – I dedicate this project to my beloved dogs Sniff, Golias, and Frederico. I miss you dearly and love you always. ❤️
        """, unsafe_allow_html=True)

st.set_page_config(layout="wide")

col1, col2 = st.columns([1.2, 2.5])  # define as colunas


# About section
with col1:
    st.markdown("""
                    <div style='
                        background-color: white;
                        border: 1px solid #ccc;
                        border-radius: 10px;
                        padding: 20px;
                        font-family: Segoe UI, sans-serif;
                        color: #333;
                        box-shadow: 0 0 4px rgba(0,0,0,0.05);
                        text-align: justify;'>
                            <p style='font-size: 15px; line-height: 1.5;'>
                                For this project, I am utilizing the dataset available at 
                                    <a href="https://www.kaggle.com/datasets/waqi786/dogs-dataset-3000-records" target="_blank">
                                        Kaggle - Dogs Dataset (3,000 records)
                                    </a>, which comprises 3,000 entries containing detailed information about dogs. 
                                This dataset includes key attributes such as breed, age, weight, color, and gender, 
                                and is particularly well-suited for studies related to canine characteristics, 
                                data analysis, and machine learning applications.
                            </p>
                            <p style='font-size: 15px;'><strong>The dataset contains the following columns:</strong></p>
                                <ul style='font-size: 15px; line-height: 1.6; padding-left: 20px;'>
                                    <li><strong>Breed</strong>: The breed of the dog (e.g., Labrador Retriever, Beagle)</li>
                                    <li><strong>Age (Years)</strong>: The dog’s age, ranging from 1 to 15 years</li>
                                    <li><strong>Weight (kg)</strong>: The dog’s weight in kilograms, ranging from 5 kg to 60 kg</li>
                                    <li><strong>Color</strong>: The dog’s color (e.g., Black, White, Brown)</li>
                                    <li><strong>Gender</strong>: The dog’s gender (Male or Female)</li>
                                </ul>
                            <p style='font-size: 15px; line-height: 1.5;'>
                                Additionally, I incorporate complementary information from 
                                <a href="https://data.europa.eu" target="_blank">data.europa.eu</a>, 
                                particularly the file <strong>zuordnungstabellehunderassehundetyp</strong>, which provides breed classification data.
                            </p>
                            <p style='font-size: 15px; line-height: 1.5;'>
                                By combining both datasets, I aim to generate relevant insights that enhance the understanding of breed distribution, 
                                demographic patterns, and correlations between variables.
                            </p>
                    </div> """, unsafe_allow_html=True)

with col2:
    option = st.selectbox("Select a chart to display:", list(graficos.keys()))
    graficos[option]()

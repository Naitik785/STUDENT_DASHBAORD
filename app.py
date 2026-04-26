import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title("MarkSheet")
st.write("File Must Have Column Name,Maths,Science,English,History")
file=st.file_uploader("Upload Your File",type=["csv"])

if file:
    df = pd.read_csv(file)
    subjects = [col for col in df.columns if col not in ["Name", "Grade"]]  # ✅
    df[subjects] = df[subjects].apply(pd.to_numeric, errors="coerce")  # ✅ add this
    df = df.dropna()
    df["Total"] = df[subjects].sum(axis=1)
    df["Average"] = df["Total"] / len(subjects)
    df["Grade"]=pd.cut(df["Average"],bins=[0,50,60,70,80,90,100],labels=["F","D","C","B","A","A+"])
    df["Pass/Fail"]=df["Average"].apply(lambda x: "Pass" if x>=50 else "Fail")

    col1,col2,col3 = st.columns(3)
    col1.metric("Total Students",len(df))
    col2.metric("Class Average", f"{df['Average'].mean():.1f}")
    col3.metric("Pass Rate", f"{(df['Pass/Fail']=='Pass').mean()*100:.1f}%")


    st.subheader("Student Record")
    st.dataframe(df)

    fig,ax=plt.subplots(figsize=(12,5))

    student=df["Name"]
    x=np.arange(len(student))

    width = 0.8 / len(subjects)
    for i, subject in enumerate(subjects):
        offset = (i - len(subjects) / 2) * width + width / 2
        ax.bar(x + offset, df[subject], width, label=subject)

    ax.set_xticks(x)
    ax.set_xticklabels(student,rotation=45)
    ax.legend()
    ax.set_title("Average Mark In Subjects")
    ax.set_ylabel("Marks")
    ax.set_xlabel("Students")
    st.pyplot(fig)

    fig2,ax2=plt.subplots()

    pass_fail=df["Pass/Fail"].value_counts()
    colors=["green" if label == "Pass" else "red" for label in pass_fail.index]

    ax2.pie(pass_fail.values,labels=pass_fail.index,colors=colors,autopct="%1.1f%%")
    ax2.set_title("Pass/Fail Distibution")
    st.pyplot(fig2)

    st.subheader("Individual Student Report")
    selected = st.selectbox("Select Student",df["Name"])
    student= df[df["Name"]==selected].iloc[0]

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Marks",f"{student['Total']}/400")
    c2.metric("Average", f"{student['Average']:.1f}")
    c3.metric("Grade", f"{student['Grade']}")
    c4.metric("Pass/Fail", f"{student['Pass/Fail']}")

    fig3,ax3 = plt.subplots()
    marks = []
    for s in subjects:
        marks.append(student[s])
    colors1=["Green" if m >= 35 else "red" for m in marks]
    ax3.bar(subjects,marks,color=colors1,edgecolor="black")
    ax3.set_title(f"{selected}'s Marks")
    ax3.set_xlabel("Subjects")
    ax3.set_ylabel("Marks")
    ax3.axhline(y=35,color="red",label="Pass Line",linestyle="--")
    ax3.legend()
    st.pyplot(fig3)










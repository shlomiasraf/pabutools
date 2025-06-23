תחילה הרצנו את 5 ניסויים של קלטים מהתיקיה experiments_csv על האלגוריתם שלנו ועל Phragmen וקיבלנו את התוצאות הבאות:

 ![execution_time_comparison](https://github.com/user-attachments/assets/85eca783-5b59-4855-a842-78ac4ba2fcd4)
כאשר: 

הניסוי experiment1.csv - מכיל 3 פרויקטים ו-4 מצביעים.

הניסוי experiment2.csv - מכיל 4 פרויקטים ו-4 מצביעים.

הניסוי experiment3.csv - מכיל 3 פרויקטים ו-6 מצביעים.

הניסוי experiment4.csv - מכיל 4 פרויקטים ו-4 מצביעים.

הניסוי experiment5.csv - מכיל 3 פרויקטים ו-4 מצביעים.

כפי שניתן לראות אלגוריתם Phragmen רץ יותר מהר על הניסויים והם החזירו את אותם פרויקטים כפלט.

לאחר מכן ביצענו שיפור באלגוריתם שלנו ע״י כך שהוספנו זיכרון מטמון לאלגוריתם ע״י הוספת השורות האלה:


        project_to_load = {}
        for p in approvers_map:
            key = (p.name, tuple(approvers_map[p]), tuple(current_loads))
            if key in load_cache:
                load = load_cache[key]
            else:
                load = compute_load(p, approvers_map[p], current_loads)
                load_cache[key] = load
            project_to_load[p] = load
שדואגת שלא נחשב שוב ושוב את ה- max load אם דבר לא השתנה.
והרצנו על קלט מאוד גדול לפני ואחרי השינוי וזה התוצאות שקיבלנו:
![gpseq_runtime_comparison](https://github.com/user-attachments/assets/3c377a49-8970-4c0d-bc14-3db43c86a2b2)

הניסוי big_input.csv - שמכיל 1000 פרויקטים ו-1000 מצביעים.
והרצנו גם על כל הניסויים ביחד:

![gpseq_runtime_lineplot](https://github.com/user-attachments/assets/8e0f7033-555e-46fa-b522-e1c0e6c55371)

משמע השינוי שיפר את זמן הריצה של האלגוריתם!
ולכן הוא שיפר ביצועים.

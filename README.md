תחילה הרצנו את 5 ניסויים של קלטים מהתיקיה experiments_csv על האלגוריתם שלנו ועל Phragmen וקיבלנו את התוצאות הבאות:

 ![execution_time_comparison](https://github.com/user-attachments/assets/85eca783-5b59-4855-a842-78ac4ba2fcd4)
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

משמע השינוי שיפר את זמן הריצה של האלגוריתם!
ולכן הוא שיפר ביצועים.

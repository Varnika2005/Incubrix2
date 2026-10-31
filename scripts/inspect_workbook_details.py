import openpyxl

wb = openpyxl.load_workbook('submission/workbook/IncuBrix_2027_Growth_Engineer_Option_3_AEO_SEO_GEO_Submission_Workbook.xlsx', data_only=False)
ws0 = wb['00_START']
print("=== 00_START ===")
for r in [5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,21,24,25,26,27]:
    f_val = ws0[f'F{r}'].value if r <= 10 else ""
    print(f"R{r} A: {ws0[f'A{r}'].value} | B: {ws0[f'B{r}'].value} | F: {f_val}")

ws4 = wb['04_SELF_CHECK']
print("\n=== 04_SELF_CHECK ===")
for r in range(5, 13):
    print(f"R{r} A: {ws4[f'A{r}'].value} | B: {ws4[f'B{r}'].value} | C: {ws4[f'C{r}'].value} | D: {ws4[f'D{r}'].value} | F: {ws4[f'F{r}'].value}")

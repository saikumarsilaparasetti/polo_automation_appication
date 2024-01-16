import pandas as pd
import os
# filename = "/Users/saikumarsilaparasetti/Downloads/polo_create_record.xlsx"
# xlsx = pd.ExcelFile(filename)
# df = pd.read_excel(filename)

# for ind in df.index:
#     try:
#         global lpmno
#         lpmno = df['lpmno'][ind]
#
#         df.at[ind, 'status'] = "Completed"
#         print("lpm NO", lpmno)
#     except Exception as e:
#         print("Exception: ", e)
# print(lpmno, "is the lpm")
# with pd.ExcelWriter(filename, engine='openpyxl') as writer:
#     df.to_excel(writer, index=False)


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'blank.pdf')
print(filename)

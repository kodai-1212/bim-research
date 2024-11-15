import os
from pyrevit import script
from pyrevit import revit, DB

# 出力先のパスを指定
output_path = r'C:\Users\harug\pyrevit\FamilyInfo.txt'

# Revitファイルを指定
revit_file_path = r'"C:\Users\harug\pyrevit\サンプル構造.rvt"'

# Revitファイルを開く
doc = revit.doc.Application.OpenDocumentFile(revit_file_path)

# ファミリー情報を取得
collector = DB.FilteredElementCollector(doc)
families = collector.OfClass(DB.Family).ToElements()

# ファミリー情報を出力
with open(output_path, 'w') as file:
    for family in families:
        file.write(f"Family Name: {family.Name}\n")
        file.write(f"Family Id: {family.Id}\n")
        file.write("---------------------------\n")

# ドキュメントを閉じる
doc.Close(False)

# 完了メッセージを表示
script.get_output().print_md("Family information has been exported successfully.")

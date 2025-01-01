from odoo import models

class PatientCardXlsx(models.AbstractModel):
    _name = 'report.hospital.action_report_patient_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        for obj in patients:
            row = 1
            col = 1
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name[:31])
            format1 = workbook.add_format(
                {'bold': True, 'border': 1,
                 'align': 'center',
                 })

            format2 = workbook.add_format({
                'font_size': 12,
                'font_color': 'black',
                'align': 'center',
            })

            sheet.set_column(row, col, 20)
            sheet.set_column(row, col + 1, 20)
            sheet.set_column(row, col + 2, 20)
            sheet.set_column(row, col + 3, 20)
            sheet.set_column(row, col + 4, 20)

            sheet.write(row, col, 'Name', format1)
            sheet.write(row, col + 1, 'Date Of Birth', format1)
            sheet.write(row,  col + 2, 'Age', format1)
            sheet.write(row,  col + 3, 'Gender', format1)
            sheet.write(row,  col + 4, 'Description', format1)
            row += 1
            sheet.write(row,  col , obj.name, format2)
            sheet.write(row,  col + 1, str(obj.date_of_birth).format('mm/dd/yy'), format2)
            sheet.write(row,  col + 2, obj.age, format2)
            sheet.write(row,  col + 3, obj.gender, format2)
            sheet.write(row,  col + 4, obj.note, format2)


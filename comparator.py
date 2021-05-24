import xlsxwriter
from filecmp import dircmp


class ExcelReporter:
    def flatten_structure(self, dir_list):
        flatten_dir = [item for sublist in dir_list for item in sublist]
        return flatten_dir

    def create_excel(self, left_dir, right_dir, report_name):
        workbook = xlsxwriter.Workbook(report_name)
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        worksheet.write('A1', 'files only in folder A', bold)
        row = 1
        flat_left_dir = self.flatten_structure(left_dir)
        for row_data in flat_left_dir:
            worksheet.write(row, 0, row_data)
            row += 1
        worksheet.write('B1', 'files only in folder B', bold)
        row = 1
        flat_right_dir = self.flatten_structure(right_dir)
        for row_data in flat_right_dir:
            worksheet.write(row, 1, row_data)
            row += 1
        workbook.close()


class DiffGenerator:

    left_dir = list()
    right_dir = list()

    def diff(self, dcmp):
        # dcmp.report()
        left = dcmp.left_only
        right = dcmp.right_only
        for sub_dcmp in dcmp.subdirs.values():
            self.left_dir.append(self.diff(sub_dcmp)[0])
            self.right_dir.append(self.diff(sub_dcmp)[1])
        return [left, right]


class DiffReporter():
    def diff_report(self, dir1='right', dir2='left', report_name='artifact.xlsx'):
        dcmp = dircmp(dir1, dir2)
        df_gen = DiffGenerator()
        df_gen.left_dir.append(df_gen.diff(dcmp)[0])
        df_gen.right_dir.append(df_gen.diff(dcmp)[1])
        excel_reporter = ExcelReporter()
        excel_reporter.create_excel(
            df_gen.left_dir, df_gen.right_dir, report_name)


if __name__ == "__main__":
    df = DiffReporter
    df.diff_report()

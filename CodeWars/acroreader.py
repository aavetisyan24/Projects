# case1 = "dwc_aux_i2c_u4ls_cuamd1_tsmc5ff12ns_databook.pdf"
# case2 = "dwc_usb31sspphy_cuamd_tsmc5ffx1ns_databook.pdf"
case3 = "dwc_hdmi21_earc_tx_ns_tsmc_16ffc18_databook.pdf"
case4 = "dwc_ap1_c10mpphy_gf22fdsoiext_x1ns_databook.pdf"
# case5 = "dwc_hdmi20_tx_ns_6gbps_tsmc_12ffc18_databook.pdf"
# case6 = "dwc_usbc31dptxphy_ss5lpe_databook.pdf"
# case7 = "dwc_32g_phy_g2_tsmc7ff_x4ns_databook.pdf"
case8 = "dwc_pcie5phy_smic12sfe_x4ns_databook.pdf"
case9 = "dwc_mipi_cd_rx_3t4l_tsmc12ffc18ns_databook.pdf"
case10 = "dwc_112g_ethernet_phy_tsmc7ff_databook.pdf"

import block_tcl_finder
import PyPDF4
from tabula import read_pdf
import pandas as pd
pd.set_option("display.max_rows", 100, "display.max_columns", 10)
pd.set_option("display.width", 320)

block_tcl_finder.find_bloc_tcl()  # will copy block.tcl to current directory
metal_in_block_tcl = block_tcl_finder.find_metal_stack()  # will find metal name from block.tcl
# print(metal_in_block_tcl)

page_number = False
page_number_metal = False
metal_pages = []

def check_lef_area_in_databook(databook):
    global page_number
    pdf = "Latest/doc/"+databook
    file = open(pdf, "rb")
    reader = PyPDF4.PdfFileReader(file)
    pages = reader.numPages

    def find_page_number_lef():
        global page_number
        text, word = "", ""
        count = 0
        for page_number_check in range(pages):
            page = reader.getPage(page_number_check)
            page_text = (page.extractText())
            for i in page_text:
                text += i
            text = (text.replace("\n", " ").replace(",","").strip().split())
            count += 1
            # print(count, text)

            """Find page with size area"""
            if (("Drawn" in text) and ("X" in text) and ("Y" in text)) and ("Table" in text) or \
               (("Drawn" in text) and ("X(µm)" in text) and ("Y(µm)" in text) and ("Table" in text)) or \
               (("Design" in text) and ("Implementation" in text) and ("Area:" in text)):
                page_number_for_area = page_number_check+1
                print("The page number for area is", page_number_for_area)
                page_number = True
                return page_number_for_area
            text = ""
        return "No page with area size"

    area_page = find_page_number_lef()
    print(area_page)
    print(page_number)

    if page_number:
        df = read_pdf(pdf, pages=area_page, encoding='utf-8', stream=True)
        with open("page_with_area.txt", "w", encoding="utf-8") as f:
            f.write(str(df))
        df = pd.DataFrame(df[0])

        print(df)
        print("############################### DATABOOK ###############################")
        print("Number of rows in area table is: ",len(df))
        print(df.columns)
        print(df.values)

        """Clear Table type1"""
        def check_unnamed_rows(data_frame):
            unnamed = False
            for i in data_frame.columns:
                if "Unnamed:" in i:
                    unnamed = True
                    print(i)

            if unnamed:
                data_frame.rename(columns=data_frame.iloc[0], inplace=True)
                data_frame.drop([0], inplace=True)
                data_frame.index = data_frame.index - 1
                print("######")
                print(data_frame)
                print("#########")

            return data_frame

        """Clear Table type2"""
        def clear_table_type2(data_frame):
            print("It is Table type 2")
            table_list = []
            io = False
            for i in data_frame.values:
                if "I/O" in i:
                    io = True
                else:
                    print("I/O is :", io)

                if io:
                    print("I/O detected")
                    for j in list(i):
                        info = str(j)
                        if str(info).startswith("Area:") or str(info).startswith("Aspect"):
                            value = info.split(" ")
                            table_list.append(value)
            print(table_list)
            all_blocks = []
            if len(table_list) != 0:
                for i in table_list:
                    for j in range(len(i)):
                        if i[j] == "Area:":
                            area = float(i[j + 1])
                        elif i[j] == "x" or i[j] == "X":
                            DrawnX, DrawnY = float(i[j - 1]), float(i[j + 1])
                all_blocks.append(["BLOCK", DrawnX, DrawnY, area])
                print(all_blocks)
                return all_blocks
            else:
                print("AREA NOT DETECTED")

        """Clear Table type3"""
        def clear_table_type3(data_frame):
            print("It is Table type 3")
            table_list_area = ["macro", "size", "Area:"]
            table_list_size = ["x", "Aspect", "Ratio:"]
            area = False
            size = False
            table_list = []
            line = []
            for i in data_frame.values:
                for j in i:
                    # print(str(j).split(" "))
                    line.append(str(j).split(" "))
            # print(line)
            for i in line:
                if not area:
                    area = all(elem in i for elem in table_list_area)
                    if area:
                        table_list.append(i)
                if not size:
                    size = all(elem in i for elem in table_list_size)
                    if size:
                        table_list.append(i)
            print("area is", area, "and size is", size)
            if area and size:
                print("Have found info in table", table_list)
                all_blocks = []
                for i in table_list:
                    for j in range(len(i)):
                        if i[j] == "Area:":
                            area = float(i[j + 1])
                        elif i[j] == "x" or i[j] == "X":
                            DrawnX, DrawnY = float(i[j - 1]), float(i[j + 1])
                all_blocks.append(["BLOCK", DrawnX, DrawnY, area])
                print(all_blocks)
                return all_blocks

            pass

        """Checking Table type"""
        all_blocks = []
        if len(df) > 5:
            print("Other Table type")
            all_blocks = clear_table_type2(df)
            print("all_blocks:", all_blocks)
            if not all_blocks:
                print("Running def clear_table_type3")
                all_blocks = clear_table_type3(df)
            return all_blocks
        else:
            df_final = check_unnamed_rows(df)
            # print(len(df_final))

            for row in range(len(df_final)):
                info = df_final.loc[row]
                print(info)
                list_info = []
                for i in info:
                    # print(i)
                    list_info.append(i)
                # print("Information from Table")
                """Check if table info starts with block, if not add 'BLOCK'"""
                try:
                    number = float(list_info[0])
                    if number:
                        list_info.insert(0, "BLOCK")
                except Exception as msg:
                    print(msg)
                print(list_info, "\n")

                """Add all rows of table to one list, will have list of list"""
                all_blocks.append(list_info)

            print(all_blocks)
            return all_blocks

    else:
        print("Page with Area doesn't founded ")

    file.close()

def check_lef_area_in_lef(lef_view):
    print("############################### Checking LEF AREA in LEF ###############################")
    leffile = block_tcl_finder.check_lef(lef_view)
    X, Y = leffile[0], leffile[1]
    xy_lef = [X, Y]
    return xy_lef

def check_lef_vs_databook(lef_area_db, lef_area_lef):
    print("############################### Cross-Check ###############################")
    """Assigne X, Y and Area to variables for further check"""
    DrawnX = float(lef_area_db[0][1])
    DrawnY = float(lef_area_db[0][2])
    DrawnArea = float(lef_area_db[0][3])
    X, Y = lef_area_lef[0], lef_area_lef[1]

    print("""Checking Databook size with .lef size""")
    if DrawnX == X and DrawnY == Y:
        print("Databook lef area has been matched with actual area in .lef file ")
    else:
        print("Databook lef area doesn't matched with actual area in .lef file")
    print("\n")

    print("""Checking calculated Area in Databook""")
    print("Drawn area in databook: ", DrawnArea)
    area = ((DrawnX*DrawnY)/1000000)
    print("Calculated in databook: ", area, "\n")
    if str(area)[0:5] == str(DrawnArea)[0:5]:
        print("Calculation is True ", area)
    else:
        print("Calculation is False ", area)


"""Search Metal Stack(s)"""

def find_metal_page(databook):
    print("******************** Searching pages with metal information ********************")
    global page_number_metal, metal_pages
    pdf = "Latest/doc/"+databook
    with open(pdf, "rb") as file:
        reader = PyPDF4.PdfFileReader(file)
        pages = reader.numPages

        def find_page_number_metal():
            global page_number_metal
            text = ""
            for page_number_check in range(4, pages):
                page = reader.getPage(page_number_check)
                page_text = (page.extractText())
                for i in page_text:
                    text += i
                text = (text.replace("\n", " ").replace(",","").strip().split())

                """Find page with metal information"""
                if ("Metal" in text) and ("Stacks" in text):
                    page_number_for_metal = page_number_check+1
                    print("Page number with Metal Stack(s) information: ", page_number_for_metal)
                    metal_pages.append(page_number_for_metal)
                    page_number_metal = True
                text = ""
            if len(metal_pages) > 0:
                print("All pages found with metal information is/are", metal_pages, "\n")
                return
            return

        find_page_number_metal()
        if page_number_metal:
            print("******************** Checking Metal Name ********************")
        else:
            print("There is/are no page with metal information, Please check manually")
            return

    if page_number_metal:
        for page in metal_pages:
            df = read_pdf(pdf, pages=page, encoding='utf-8', stream=True)
            with open("page_with_metal.txt", "w", encoding="utf-8") as f:
                f.write(str(df))
                print("Page with Metal Stack(s) information has been saved under 'page_with_metal.txt' file in "
                      "current directory")
            # df = pd.DataFrame(df)
            # print(df)

def find_metal(metal):
    lst1 = []
    text = ""
    print("******************** Reading 'page_with_metal.txt' file to find Metal Stack(s) ********************")
    try:
        with open("page_with_metal.txt", "r") as f:
            df = pd.DataFrame(f)
    except Exception as e:
        print(e)

    lst1.append(str(df.values))
    # print(lst1)
    for i in lst1[0]:
        text += i
    text = (text.replace("\n", " ").replace(",", "").strip().split())
    for k in text:
        if str(metal) in k:
            print("Metal Stack(s) in page:", metal)
            return metal
        else:
            print("No correct Metal Stack(s) in databook, please check manual")
            return

"""End Metal Stack(s) Searching """


def main():
    databook = case3
    lef_view = "pma"
    # databook = input("Enter Databook name: ")
    # lef_view = input("Enter lef_view name: ")
    lef_area_db = check_lef_area_in_databook(databook)
    lef_area_lef = check_lef_area_in_lef(lef_view)
    print()
    print("############################### AREA: LEF vs Databook ###############################")
    print("Lef area in Databook file is ", lef_area_db)
    print("Lef area in .lef file is ", lef_area_lef)
    print()
    if lef_area_db and lef_area_lef:
        check_lef_vs_databook(lef_area_db, lef_area_lef)
    else:
        print("Nothing to check")
    """Metal Stack(s)"""
    find_metal_page(databook)
    find_metal(metal_in_block_tcl)



if __name__ == "__main__":
    main()


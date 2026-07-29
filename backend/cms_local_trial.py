import os
import time
from playwright.sync_api import sync_playwright

def run_cms_automation():
    with sync_playwright() as p:
        print("[*] Launching visible local browser window...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        
        # --- PHASE 1: LOGIN & OTP SCREEN DETECTION ---
        tab1 = context.new_page()
        print("[*] Navigating to the CMS Report entry link...")
        target_link = "https://cms.indianrail.gov.in/CMSREPORT/JSP/rpt/LoginAction.do?hmode=login&isResponsive=Y"
        tab1.goto(target_link)
        
        # Wait for overlay layout scripts to load completely
        time.sleep(3)
        
        # Dismiss the overlay by clicking center screen
        print("[*] Simulating mouse click to clear overlay screen...")
        tab1.mouse.click(500, 500)
        time.sleep(1)
        
        print("\n[!] ACTION REQUIRED: Please manually enter your User ID, Password, and Captcha.")
        print("[!] Click the blue 'Login' button when done.")
        
        # Watch for the OTP element to appear after your manual login submission
        login_detected = False
        while not login_detected:
            try:
                if tab1.locator("text=Enter OTP").is_visible():
                    print("\n[+] Success! Script detected the OTP element on the screen.")
                    login_detected = True
                else:
                    time.sleep(0.5)
            except Exception:
                time.sleep(0.5)
        
        # Quick 5-second stabilization pause
        print("[*] Starting 5-second stabilization delay...")
        time.sleep(5)
        
        # --- PHASE 2: TRUE BROWSER BYPASS DUPLICATION ---
        print("[*] Triggering OTP bypass via verified link...")
        bypass_link = "https://cms.indianrail.gov.in/CMSREPORT/JSP/rpt/LoginAction.do?hmode=skipMapHrmsId&isResponsive=Y#"
        
        # Open Tab 2
        tab2 = context.new_page()
        tab2.goto(bypass_link)
        
        # Let the session transfer fully before touching anything
        print("[*] Allowing session handshake to stabilize (5 seconds)...")
        time.sleep(5)
        
        # Close the original OTP screen tab safely
        print("[*] Closing the original OTP tab (Tab 1)...")
        tab1.close()
        
        # --- PHASE 3: SIDEBAR MENU NAVIGATION ---
        print("[*] Waiting for the dashboard sidebar to load...")
        sidebar_crew = tab2.locator("//*[text()='CREW' and not(@id='crew-btn')]").first
        sidebar_crew.wait_for(state="visible", timeout=30000)
        
        print("[*] Clicking on the correct sidebar 'CREW' menu item...")
        sidebar_crew.click()
        
        print("[*] Clicking on 'Crew Accountability' from the dropdown...")
        crew_accountal_link = tab2.get_by_role("link", name="Crew Accountal").first
        crew_accountal_link.wait_for(state="visible", timeout=10000)
        crew_accountal_link.click()
        
        # --- PHASE 4: PARAMETER CONFIGURATION ---
        print("[*] Configuring report parameter selections...")
        time.sleep(2) 
        
        # Checkboxes: Working method for ALP and SALP. LPG remains untouched.
        for designation in ["ALP", "SALP"]:
            try:
                label_locator = tab2.locator(f"label:has-text('{designation}')").first
                if label_locator.is_visible():
                    print(f"[*] Clicking working visual text label for: {designation}")
                    label_locator.click(force=True)
                else:
                    tab2.get_by_text(designation).first.click(force=True)
                time.sleep(0.4)
            except Exception as box_err:
                print(f"[!] Warning: Could not select designation {designation}: {box_err}")
        
        print("[+] Kept default LPG selection untouched.")
        
        # Radio Button: Selecting the DIVISION option via strict XPath text label matching
        print("[*] Selecting 'DIVISION' report level...")
        division_label = tab2.locator("//label[contains(text(),'DIVISION') or @for='performanceBoardDivisionLevel']").first
        division_label.wait_for(state="visible", timeout=10000)
        division_label.click(force=True)
        print("[+] DIVISION successfully selected!")
        
        time.sleep(0.5)
        
        # Click the blue Show Report button
        print("[*] Clicking 'Show Report'...")
        tab2.locator("text=Show Report").click()
        
        # --- PHASE 5: SUMMARY TABLE INTERACTION ---
        print("[*] Waiting for the summary table data wrapper to load...")
        tab2.locator("text=COMPLETE CREW ACCOUNTAL REPORT FOR").wait_for(state="visible", timeout=45000)
        time.sleep(3) 
        
        print("[*] Directly extracting the clickable link element from the summary table rows...")
        total_link = tab2.locator("table.dataTable a, .dataTables_wrapper table a").last
        total_link.wait_for(state="visible", timeout=15000)
        
        print(f"[*] Clicking dynamic total link element...")
        total_link.click()
        
        # --- PHASE 6: DETAILED EXPANSION & ALL DROPDOWN ---
        print("[*] Total link clicked. Waiting 30 seconds for initial breakdown load...")
        time.sleep(30)
        
        print("[*] Locating the LOWER 'Display' records selection box...")
        lower_dropdown = tab2.locator("select[name='example_length']").last
        if not lower_dropdown.is_visible():
            lower_dropdown = tab2.locator("div.dataTables_length select").last
            
        print("[*] Selecting 'All' rows option from the dropdown...")
        lower_dropdown.select_option("All")
        
        print("[*] 'All' selected. Waiting 30 seconds for the entire dataset to render...")
        time.sleep(30)
        
        # --- PHASE 7: EXPORT FINAL REPORT ---
        print("[*] Locating the LOWER green Excel export button...")
        lower_excel_btn = tab2.locator("text=Excel").last
        
        print("[*] Triggering download via lower Excel button...")
        with tab2.expect_download() as download_info:
            lower_excel_btn.click()
            
        download = download_info.value
        
        # Dynamically map your desktop route perfectly
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        save_path = os.path.join(desktop_path, download.suggested_filename)
        
        download.save_as(save_path)
        print(f"\n[=== SUCCESS ===]\nYour file has been extracted successfully and saved to: {save_path}")
        
        print("\nPress Enter here in this black command prompt window to close the browser session...")
        input()
        browser.close()

if __name__ == "__main__":
    run_cms_automation()
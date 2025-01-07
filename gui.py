import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from s3_scanner import S3Scanner
from iam_policy_analyzer import IAMPolicyAnalyzer  # Updated import
from reports import ReportManager
from alerts import SecurityAlerts
import json


class SecurityScannerGUI:
    def __init__(self, root):
        self.s3_scanner = S3Scanner()
        self.iam_analyzer = IAMPolicyAnalyzer()
        self.report_manager = ReportManager()
        self.alerts = SecurityAlerts(
            email_sender="your_email@gmail.com",
            email_password="your_password",
            email_receiver="receiver_email@gmail.com"
        )

        self.buckets = {
            "General Data": "gendatavaultbucket",
            "Logs": "logsvaultbucket",
            "Sensitive Data": "sensitivevaultbucket",
        }

        self.root = root
        self.root.title("AWS Security Scanner")

        # Dropdown for buckets
        tk.Label(root, text="Select Bucket:").grid(row=0, column=0, padx=10, pady=5)
        self.selected_bucket = tk.StringVar(root)
        self.selected_bucket.set(list(self.buckets.keys())[0])  # Default selection
        tk.OptionMenu(root, self.selected_bucket, *self.buckets.keys()).grid(row=0, column=1, padx=10, pady=5)

        # Buttons
        scan_button = tk.Button(root, text="Scan Bucket", command=self.scan_bucket)
        scan_button.grid(row=0, column=2, padx=10, pady=5)

        policy_button = tk.Button(root, text="Analyze IAM Policy", command=self.analyze_policy)
        policy_button.grid(row=1, column=1, pady=5)

        # Output Box
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
        self.output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def scan_bucket(self):
        bucket_type = self.selected_bucket.get()
        bucket_name = self.buckets[bucket_type]

        results = self.s3_scanner.scan_bucket(bucket_name)
        self.report_manager.store_report(bucket_name, results)

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Results for {bucket_name} ({bucket_type}):\n\n")
        self.output_text.insert(tk.END, "\n".join(results))

        # Trigger alerts for sensitive data bucket
        if bucket_type == "Sensitive Data":
            for issue in results:
                self.alerts.send_alert(f"Sensitive Issue in {bucket_name}: {issue}")

    def analyze_policy(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, 'r') as f:
                policy = json.load(f)
                results = self.iam_analyzer.analyze_policy(policy)
                self.report_manager.store_report("IAM Policy", results)

                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "Results for IAM Policy:\n\n")
                self.output_text.insert(tk.END, "\n".join(results))

                for issue in results:
                    self.alerts.send_alert(issue)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze policy: {e}")

class Payroll:
    def __init__(self, user_id, name, job, salary):
        self.UserID = user_id
        self.Name = name
        self.Job = job
        self.Salary = salary

    def __repr__(self):
        return f"Payroll({self.UserID}, {self.Name}, {self.Job}, {self.Salary})"

examples = [
    Payroll(1, "John Doe", "Software Engineer", 70000),
    Payroll(2, "Jane Smith", "Data Scientist", 80000),
    Payroll(3, "Alice Johnson", "Product Manager", 90000),
    Payroll(4, "Bob Brown", "UX Designer", 60000),
    Payroll(5, "Charlie Davis", "DevOps Engineer", 75000)
]

for p in examples:
    print(p)


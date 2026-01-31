import os

HEADER_MAP = {
    'Account.csv': 'accountId:ID(aid)|createTime:LONG|isBlocked:BOOLEAN|accountType|nickname|phonenum|email|freqLoginType|lastLoginTime|accountLevel',
    'Loan.csv': 'loanId:ID(lid)|loanAmount:DOUBLE|balance:DOUBLE|createTime:LONG|loanUsage|interestRate:DOUBLE',
    'Medium.csv': 'mediumId:ID(mid)|mediumType|isBlocked:BOOLEAN|createTime:LONG|lastLoginTime|riskLevel',
    'Person.csv': 'personId:ID(pid)|personName|isBlocked:BOOLEAN|createTime:LONG|gender|birthday|country|city',
    'AccountTransferAccount.csv': 'fromId:START_ID(aid)|toId:END_ID(aid)|amount:DOUBLE|createTime:LONG|orderNum:LONG|comment|payType|goodsType',
    'MediumSignInAccount.csv': 'mediumId:START_ID(mid)|accountId:END_ID(aid)|createTime:LONG|location|comment',
    'PersonOwnAccount.csv': 'personId:START_ID(pid)|accountId:END_ID(aid)|createTime:LONG|comment',
    'LoanDepositAccount.csv': 'loanId:START_ID(lid)|accountId:END_ID(aid)|amount:DOUBLE|createTime:LONG|comment',
    'PersonGuaranteePerson.csv': 'fromId:START_ID(pid)|toId:END_ID(pid)|createTime:LONG|relation|comment',
    'PersonApplyLoan.csv': 'personId:START_ID(pid)|loanId:END_ID(lid)|loanAmount:DOUBLE|createTime:LONG|org|comment'
}

def update_first_line(file_path, new_header):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if content == '':
            print(f"⚠️  File is empty, skipping: {file_path}")
            return

        # Split by lines
        lines = content.splitlines()
        
        # Replace the first line
        lines[0] = new_header

        # Write back, preserving original newline style (or unify to \n)
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ Updated first line: {file_path}")

    except Exception as e:
        print(f"❌ Update failed {file_path}: {e}")

def main():
    # Current directory, you can change it to your own path
    base_dir = '../scratch/import/'
    
    for filename, new_header in HEADER_MAP.items():
        file_path = os.path.join(base_dir, filename)
        update_first_line(file_path, new_header)

if __name__ == '__main__':
    main()

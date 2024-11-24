import os
from mistralai import Mistral

class MistralService:
    def __init__(self):
        self.client = Mistral(api_key="FzY030wCon5Up9jSKpPusux9cvxCsrCN")
        self.model = "mistral-medium"

    def analyze_file(self, text):
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Hi i have a financial model in excel. I have converted the excel model calculation into formulas. I have written logic in format: label of associated with the cell, address of the cell, cell value, formula in Excel format and formula with labels to what they refer to. Can you review formulas if they are correct in terms of common finance logic. Please highlight incorrect and correct results right away. Can you give me a result in a table with calculation names (referred as labels above) as rows and comments in a column to the side. Display this in proper markdown please.\n\n{text}"
                }
            ]
        )

        return chat_response.choices[0].message.content     
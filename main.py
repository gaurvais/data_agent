from agents.data_agent import data_agent
from langchain_core.messages import HumanMessage

if __name__ == "__main__":

    response = data_agent.invoke(
        {"messages":[HumanMessage(content="What are the different types of Payment Methods we have in our database?")],
         "route_response": ""}
    )

    # response = data_agent.invoke(
    #     {"messages":[HumanMessage(content="I want to extract the data from the API endpoint 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,binancecoin,ripple,cardano,dogecoin,polkadot,avalanche-2,chainlink&vs_currencies=usd' and save it to data/extract folder in the csv folder")],
    #      "route_response": ""}
    # )

    print(response)
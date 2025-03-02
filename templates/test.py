import pickle

# Load the model
with open("final_model_pipeline.pkl", "rb") as file:
    model = pickle.load(file)

# Print the type of the loaded object
print("Loaded model type:", type(model))

import numpy as np
import os
def PredictFumenLevel(factors, Course, Reference, Model):
    match Course:
        case "Oni/Edit":
            path = "model/Oni_Edit/"
            match Reference:
                case "AC14":
                    ModelName = "14_"
                    match Model:
                        case "1 - 1 layer (Linear)":                    #cost 0.76
                            w = np.array([ 0.008, -0.658,  0.564,  0.237, -0.249, -0.042,  0.177, -0.005, -0.300, -0.010,  1.255])
                            b = 0.22802430773477664
                            return Model_1_layer(factors, w, b)    
                        case "2 - 1 layer (20 Sigmoids)":               #cost 0.53
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_1_layer_WithActivFunc(factors, path, "Sigmoids", 20)
                        case "3 - 1 layer (11 HardSigmoids)":           #cost 0.57
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_1_layer_WithActivFunc(factors, path, "Hardsigmoid", 11)
                        case "4 - 3 layers (Linear with ReLUs)":        #cost 0.65
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_3_layers(factors, path)
                        case "5 - 4 layers (Linear with ReLUs)":        #cost 0.62
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_4_layers(factors, path)
                        case _: return None
                case "AC15.0":
                    ModelName = "15_"
                    match Model:
                        case "1 - 1 layer (Linear)":                    #cost 0.500
                            w = np.array([0.00804691, -2.0588207, 0.25349426, 0.39613602, -0.11540893, -0.01972612, 0.3689399, -0.00670579, 0.1935756, 0.29895967, 1.0127863])
                            b = 1.3593606
                            return Model_1_layer(factors, w, b)    
                        case "2 - 1 layer (20 Sigmoids)":               #cost 0.407
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_1_layer_WithActivFunc(factors, path, "Sigmoids", 20)
                        case "3 - 1 layer (11 HardSigmoids)":           #cost 0.435
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_1_layer_WithActivFunc(factors, path, "Hardsigmoid", 11)
                        case "4 - 2 layers (Linear with ReLUs)":        #cost 0.499
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_2_layers(factors, path)
                        case "5 - 4 layers (Linear with ReLUs)":        #cost 0.355
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_4_layers(factors, path)
                        case _: return None
                case "wii4":
                    ModelName = "wii4_"
                    match Model:
                        case "1 - 1 layer (Linear)":                    #cost 0.975
                            w = np.array([0.01356443, -0.6947324, 0.52886003, 0.36182046, -0.02143821, -0.04352877, -0.2709177, -0.0031311, -0.07876872, -0.1567187, 0.44459754])
                            b = 1.1612875
                            return Model_1_layer(factors, w, b)    
                        case "2 - 1 layer (20 Sigmoids)":               #cost 0.589
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_1_layer_WithActivFunc(factors, path, "Sigmoids", 20)
                        case "3 - 1 layer (11 HardSigmoids)":           #cost 0.556
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_1_layer_WithActivFunc(factors, path, "Hardsigmoid", 11)
                        case "4 - 4 layers (Linear with ReLUs)":        #cost 0.686
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_4_layers(factors, path)
                        case "5 - 11 layers (Linear with ReLUs)":       #cost 0.360
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_11_layers(factors, path)
                        case _: return None
                case _: return None
        case "Hard":
            path = "model/Hard/"
            match Reference:
                case "wii4":
                    ModelName = "wii4_"
                    match Model:
                        case "1 - 1 layer (Linear)":                    #cost 0.74
                            w = np.array([0.0165925, -0.6558655, 0.48939788, 0.09709357, 0.01883165, 0.20487629, -0.4718081, 0.00014644, -0.01825179, 0.5021678, 0.14833954])
                            b = -0.11671088
                            return Model_1_layer(factors, w, b)    
                        case _: return None
                case _: return None
        case "Normal":
            path = "model/Normal/"
            match Reference:
                case "wii4":
                    ModelName = "wii4_"
                    match Model:
                        case "1 - 11 layers (Linear with ReLUs)":       #cost 0.434
                            path = path + ModelName + Model[0] + ".pth"
                            return Model_11_layers(factors, path)
                        case _: return None
                case _: return None
        case "Easy":
            path = "model/Easy/"
            match Reference:
                case "wii4":
                    ModelName = "wii4_"
                    match Model:
                        case "1 - 1 layer (Linear)":                    #cost 0.522
                            w = np.array([0.00667484, 0.8297021, 1.0193855, -0.14305532, -0.5054439, 0.13404506, 0.6024903, 0.00616904, -0.0020158, 0.6182017, 0.62950253])
                            b = -0.78795093
                            return Model_1_layer(factors, w, b)    
                        case _: return None
                case _: return None
        case _: return None

def Reduced_file_path(Og_path):
    New = ""
    for char in Og_path:
        if(char!="/"):
            New = New + char
        else:
            New = ""
    return New

def Model_1_layer(factors, weights, bias):
    return np.dot(factors,weights) + bias
def Model_2_layers(factors, ModelPath):
    import torch
    from torch import nn
    factors = torch.from_numpy(factors)
    factors = factors.type(torch.float32)
    if(not os.path.isfile(ModelPath)):
      raise Exception(f"Your option need model file \"{Reduced_file_path(ModelPath)}\"  , but it doesn't exist.")

    class LinearRegressionModel(nn.Module):
      def __init__(self):
        super().__init__()
        self.layer_stack = nn.Sequential \
          (
            nn.Linear(in_features=11, out_features=5),
            nn.ReLU(),
            nn.Linear(in_features=5, out_features=1)
          )
      def forward(self, x):
        return (self.layer_stack(x)).type(torch.float64)

    TaikoLevelModel = LinearRegressionModel()
    TaikoLevelModel.load_state_dict(torch.load(f=ModelPath))

    TaikoLevelModel.eval()
    with torch.inference_mode():
      predict_level = TaikoLevelModel(factors)

    factors = factors.reshape(-1)
    predict_level = predict_level.numpy()
    predict_level = predict_level.tolist()[0]
    return predict_level
def Model_3_layers(factors, ModelPath):
    import torch
    from torch import nn
    factors = torch.from_numpy(factors)
    factors = factors.type(torch.float32)
    if(not os.path.isfile(ModelPath)):
      raise Exception(f"Your option need model file \"{Reduced_file_path(ModelPath)}\"  , but it doesn't exist.")

    class LinearRegressionModel(nn.Module):
      def __init__(self):
        super().__init__()
        self.layer_stack = nn.Sequential \
          (
            nn.Linear(in_features=11, out_features=7),
            nn.ReLU(),
            nn.Linear(in_features=7, out_features=3),
            nn.ReLU(),
            nn.Linear(in_features=3, out_features=1)
          )
      def forward(self, x):
        return (self.layer_stack(x)).type(torch.float64)

    TaikoLevelModel = LinearRegressionModel()
    TaikoLevelModel.load_state_dict(torch.load(f=ModelPath))

    TaikoLevelModel.eval()
    with torch.inference_mode():
      predict_level = TaikoLevelModel(factors)

    factors = factors.reshape(-1)
    predict_level = predict_level.numpy()
    predict_level = predict_level.tolist()[0]
    return predict_level
def Model_4_layers(factors, ModelPath):
    import torch
    from torch import nn
    factors = torch.from_numpy(factors)
    factors = factors.type(torch.float32)
    if(not os.path.isfile(ModelPath)):
      raise Exception(f"Your option need model file \"{Reduced_file_path(ModelPath)}\"  , but it doesn't exist.")

    class LinearRegressionModel(nn.Module):
      def __init__(self):
        super().__init__()
        self.layer_stack = nn.Sequential \
          (
            nn.Linear(in_features=11, out_features=7),
            nn.ReLU(),
            nn.Linear(in_features=7, out_features=5),
            nn.ReLU(),
            nn.Linear(in_features=5, out_features=3),
            nn.ReLU(),
            nn.Linear(in_features=3, out_features=1)
          )
      def forward(self, x):
        return (self.layer_stack(x)).type(torch.float64)

    TaikoLevelModel = LinearRegressionModel()
    TaikoLevelModel.load_state_dict(torch.load(f=ModelPath))

    TaikoLevelModel.eval()
    with torch.inference_mode():
      predict_level = TaikoLevelModel(factors)

    factors = factors.reshape(-1)
    predict_level = predict_level.numpy()
    predict_level = predict_level.tolist()[0]
    return predict_level
def Model_11_layers(factors, ModelPath):
    import torch
    from torch import nn
    factors = torch.from_numpy(factors)
    factors = factors.type(torch.float32)
    if(not os.path.isfile(ModelPath)):
      raise Exception(f"Your option need model file \"{Reduced_file_path(ModelPath)}\"  , but it doesn't exist.")

    class LinearRegressionModel(nn.Module):
      def __init__(self):
        super().__init__()
        self.layer_stack = nn.Sequential \
          (
            nn.Linear(in_features=11, out_features=10),
            nn.ReLU(),
            nn.Linear(in_features=10, out_features=9),
            nn.ReLU(),
            nn.Linear(in_features=9, out_features=8),
            nn.ReLU(),
            nn.Linear(in_features=8, out_features=7),
            nn.ReLU(),
            nn.Linear(in_features=7, out_features=6),
            nn.ReLU(),
            nn.Linear(in_features=6, out_features=5),
            nn.ReLU(),
            nn.Linear(in_features=5, out_features=4),
            nn.ReLU(),
            nn.Linear(in_features=4, out_features=3),
            nn.ReLU(),
            nn.Linear(in_features=3, out_features=2),
            nn.ReLU(),
            nn.Linear(in_features=2, out_features=1),
            nn.ReLU(),
          )

      def forward(self, x):
        return (self.layer_stack(x)).type(torch.float64)

    TaikoLevelModel = LinearRegressionModel()
    TaikoLevelModel.load_state_dict(torch.load(f=ModelPath))

    TaikoLevelModel.eval()
    with torch.inference_mode():
      predict_level = TaikoLevelModel(factors)

    factors = factors.reshape(-1)
    predict_level = predict_level.numpy()
    predict_level = predict_level.tolist()[0]
    return predict_level
def Model_1_layer_WithActivFunc(factors, ModelPath, ActivFunc, ActivFuncNum):
    import torch
    from torch import nn
    factors = torch.from_numpy(factors)
    factors = factors.type(torch.float32)
    if(not os.path.isfile(ModelPath)):
      raise Exception(f"Your option need model file \"{Reduced_file_path(ModelPath)}\"  , but it doesn't exist.")

    class LinearRegressionModel(nn.Module):
      def __init__(self):
        super().__init__()
        self.active_func_num = ActivFuncNum
        self.inputfeat_num = 11

        self.c = nn.Parameter(torch.rand(self.active_func_num, requires_grad=True))
        self.w = nn.Parameter(torch.rand(self.active_func_num, self.inputfeat_num, requires_grad=True))
        self.b = nn.Parameter(torch.rand(1, requires_grad=True))
        self.b_inside = nn.Parameter(torch.rand(self.active_func_num, requires_grad=True))

        self.sigmoid = nn.Sigmoid()
        self.hardsigmoid = nn.Hardsigmoid()

        Activate_Function = {"Sigmoids": self.sigmoid, "Hardsigmoid": self.hardsigmoid}
        self.active_func = Activate_Function[ActivFunc]

      def forward(self, x):
        Total = self.b
        for i in range(self.active_func_num):
          Total = Total + self.active_func((self.b_inside[i] + self.c[i] * ( (self.w[i]*x).sum(axis=1) )*(10**(-4))))
        return Total.type(torch.float64)

    TaikoLevelModel = LinearRegressionModel()
    TaikoLevelModel.load_state_dict(torch.load(f=ModelPath))

    TaikoLevelModel.eval()
    with torch.inference_mode():
      predict_level = TaikoLevelModel(factors.reshape(1,-1))

    factors = factors.reshape(-1)
    predict_level = predict_level.numpy()
    predict_level = predict_level.tolist()[0]
    return predict_level


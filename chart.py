import re
import matplotlib.pyplot as plt

# The text data containing the training history
log_data = """
Epoch 0002 | Train Loss: 0.1241 | Val Loss: 0.1225 | Perfect Match Accuracy: 0.00%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0003 | Train Loss: 0.1217 | Val Loss: 0.1209 | Perfect Match Accuracy: 0.00%
Epoch 0004 | Train Loss: 0.1204 | Val Loss: 0.1198 | Perfect Match Accuracy: 0.00%
Epoch 0005 | Train Loss: 0.1195 | Val Loss: 0.1191 | Perfect Match Accuracy: 0.00%
Epoch 0006 | Train Loss: 0.1188 | Val Loss: 0.1181 | Perfect Match Accuracy: 0.00%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0007 | Train Loss: 0.1177 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.00%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0008 | Train Loss: 0.1168 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.01%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0009 | Train Loss: 0.1163 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.01%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0010 | Train Loss: 0.1159 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.01%
Epoch 0011 | Train Loss: 0.1155 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.01%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0012 | Train Loss: 0.1153 | Val Loss: 0.1150 | Perfect Match Accuracy: 0.01%
Epoch 0013 | Train Loss: 0.1151 | Val Loss: 0.1148 | Perfect Match Accuracy: 0.01%
Epoch 0014 | Train Loss: 0.1152 | Val Loss: 0.1149 | Perfect Match Accuracy: 0.01%
Epoch 0015 | Train Loss: 0.1151 | Val Loss: 0.1148 | Perfect Match Accuracy: 0.01%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0016 | Train Loss: 0.1150 | Val Loss: 0.1147 | Perfect Match Accuracy: 0.01%
Epoch 0017 | Train Loss: 0.1149 | Val Loss: 0.1145 | Perfect Match Accuracy: 0.01%
Epoch 0018 | Train Loss: 0.1148 | Val Loss: 0.1145 | Perfect Match Accuracy: 0.01%
Epoch 0019 | Train Loss: 0.1147 | Val Loss: 0.1144 | Perfect Match Accuracy: 0.01%
Epoch 0020 | Train Loss: 0.1147 | Val Loss: 0.1142 | Perfect Match Accuracy: 0.01%
Epoch 0021 | Train Loss: 0.1145 | Val Loss: 0.1140 | Perfect Match Accuracy: 0.01%
Epoch 0022 | Train Loss: 0.1144 | Val Loss: 0.1139 | Perfect Match Accuracy: 0.01%
Epoch 0023 | Train Loss: 0.1143 | Val Loss: 0.1137 | Perfect Match Accuracy: 0.01%
Epoch 0024 | Train Loss: 0.1142 | Val Loss: 0.1136 | Perfect Match Accuracy: 0.01%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0025 | Train Loss: 0.1142 | Val Loss: 0.1136 | Perfect Match Accuracy: 0.02%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0026 | Train Loss: 0.1143 | Val Loss: 0.1136 | Perfect Match Accuracy: 0.01%
Epoch 0027 | Train Loss: 0.1144 | Val Loss: 0.1135 | Perfect Match Accuracy: 0.02%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0028 | Train Loss: 0.1147 | Val Loss: 0.1135 | Perfect Match Accuracy: 0.02%
Epoch 0029 | Train Loss: 0.1150 | Val Loss: 0.1135 | Perfect Match Accuracy: 0.02%
Epoch 0030 | Train Loss: 0.1148 | Val Loss: 0.1133 | Perfect Match Accuracy: 0.03%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0031 | Train Loss: 0.1147 | Val Loss: 0.1135 | Perfect Match Accuracy: 0.03%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0032 | Train Loss: 0.1147 | Val Loss: 0.1133 | Perfect Match Accuracy: 0.03%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0033 | Train Loss: 0.1148 | Val Loss: 0.1132 | Perfect Match Accuracy: 0.02%
Epoch 0034 | Train Loss: 0.1149 | Val Loss: 0.1131 | Perfect Match Accuracy: 0.03%
Epoch 0035 | Train Loss: 0.1150 | Val Loss: 0.1131 | Perfect Match Accuracy: 0.02%
Epoch 0036 | Train Loss: 0.1150 | Val Loss: 0.1131 | Perfect Match Accuracy: 0.03%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0037 | Train Loss: 0.1150 | Val Loss: 0.1131 | Perfect Match Accuracy: 0.03%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0038 | Train Loss: 0.1153 | Val Loss: 0.1134 | Perfect Match Accuracy: 0.03%
Epoch 0039 | Train Loss: 0.1164 | Val Loss: 0.1141 | Perfect Match Accuracy: 0.03%
Epoch 0040 | Train Loss: 0.1182 | Val Loss: 0.1146 | Perfect Match Accuracy: 0.03%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0041 | Train Loss: 0.1180 | Val Loss: 0.1143 | Perfect Match Accuracy: 0.03%
Epoch 0042 | Train Loss: 0.1181 | Val Loss: 0.1146 | Perfect Match Accuracy: 0.02%
Epoch 0043 | Train Loss: 0.1193 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.02%
Epoch 0044 | Train Loss: 0.1201 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.03%
Epoch 0045 | Train Loss: 0.1203 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.02%
Epoch 0046 | Train Loss: 0.1220 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.03%
Epoch 0047 | Train Loss: 0.1176 | Val Loss: 0.1142 | Perfect Match Accuracy: 0.04%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0048 | Train Loss: 0.1162 | Val Loss: 0.1135 | Perfect Match Accuracy: 0.05%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0049 | Train Loss: 0.1153 | Val Loss: 0.1134 | Perfect Match Accuracy: 0.04%
Epoch 0050 | Train Loss: 0.1146 | Val Loss: 0.1125 | Perfect Match Accuracy: 0.05%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0051 | Train Loss: 0.1142 | Val Loss: 0.1122 | Perfect Match Accuracy: 0.06%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0052 | Train Loss: 0.1138 | Val Loss: 0.1116 | Perfect Match Accuracy: 0.07%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0053 | Train Loss: 0.1132 | Val Loss: 0.1113 | Perfect Match Accuracy: 0.06%
Epoch 0054 | Train Loss: 0.1130 | Val Loss: 0.1110 | Perfect Match Accuracy: 0.10%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0055 | Train Loss: 0.1129 | Val Loss: 0.1107 | Perfect Match Accuracy: 0.10%
Epoch 0056 | Train Loss: 0.1125 | Val Loss: 0.1103 | Perfect Match Accuracy: 0.12%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0057 | Train Loss: 0.1123 | Val Loss: 0.1103 | Perfect Match Accuracy: 0.10%
Epoch 0058 | Train Loss: 0.1123 | Val Loss: 0.1100 | Perfect Match Accuracy: 0.11%
Epoch 0059 | Train Loss: 0.1123 | Val Loss: 0.1100 | Perfect Match Accuracy: 0.12%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0060 | Train Loss: 0.1123 | Val Loss: 0.1099 | Perfect Match Accuracy: 0.13%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0061 | Train Loss: 0.1123 | Val Loss: 0.1097 | Perfect Match Accuracy: 0.13%
Epoch 0062 | Train Loss: 0.1124 | Val Loss: 0.1097 | Perfect Match Accuracy: 0.13%
Epoch 0063 | Train Loss: 0.1122 | Val Loss: 0.1097 | Perfect Match Accuracy: 0.15%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0064 | Train Loss: 0.1123 | Val Loss: 0.1095 | Perfect Match Accuracy: 0.14%
Epoch 0065 | Train Loss: 0.1121 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.16%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0066 | Train Loss: 0.1121 | Val Loss: 0.1093 | Perfect Match Accuracy: 0.14%
Epoch 0067 | Train Loss: 0.1123 | Val Loss: 0.1093 | Perfect Match Accuracy: 0.15%
Epoch 0068 | Train Loss: 0.1124 | Val Loss: 0.1094 | Perfect Match Accuracy: 0.16%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0069 | Train Loss: 0.1123 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.16%
Epoch 0070 | Train Loss: 0.1122 | Val Loss: 0.1091 | Perfect Match Accuracy: 0.15%
Epoch 0071 | Train Loss: 0.1123 | Val Loss: 0.1091 | Perfect Match Accuracy: 0.17%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0072 | Train Loss: 0.1124 | Val Loss: 0.1089 | Perfect Match Accuracy: 0.18%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0073 | Train Loss: 0.1123 | Val Loss: 0.1089 | Perfect Match Accuracy: 0.18%
Epoch 0074 | Train Loss: 0.1124 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.15%
Epoch 0075 | Train Loss: 0.1126 | Val Loss: 0.1091 | Perfect Match Accuracy: 0.15%
Epoch 0076 | Train Loss: 0.1130 | Val Loss: 0.1095 | Perfect Match Accuracy: 0.15%
Epoch 0077 | Train Loss: 0.1137 | Val Loss: 0.1096 | Perfect Match Accuracy: 0.15%
Epoch 0078 | Train Loss: 0.1131 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.15%
Epoch 0079 | Train Loss: 0.1125 | Val Loss: 0.1090 | Perfect Match Accuracy: 0.16%
Epoch 0080 | Train Loss: 0.1122 | Val Loss: 0.1090 | Perfect Match Accuracy: 0.17%
Epoch 0081 | Train Loss: 0.1120 | Val Loss: 0.1088 | Perfect Match Accuracy: 0.16%
Epoch 0082 | Train Loss: 0.1121 | Val Loss: 0.1089 | Perfect Match Accuracy: 0.17%
Epoch 0083 | Train Loss: 0.1121 | Val Loss: 0.1089 | Perfect Match Accuracy: 0.17%
Epoch 0084 | Train Loss: 0.1124 | Val Loss: 0.1090 | Perfect Match Accuracy: 0.15%
Epoch 0085 | Train Loss: 0.1125 | Val Loss: 0.1091 | Perfect Match Accuracy: 0.16%
Epoch 0086 | Train Loss: 0.1127 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.15%
Epoch 0087 | Train Loss: 0.1129 | Val Loss: 0.1093 | Perfect Match Accuracy: 0.15%
Epoch 0088 | Train Loss: 0.1130 | Val Loss: 0.1094 | Perfect Match Accuracy: 0.16%
Epoch 0089 | Train Loss: 0.1131 | Val Loss: 0.1094 | Perfect Match Accuracy: 0.16%
Epoch 0090 | Train Loss: 0.1129 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.16%
Epoch 0091 | Train Loss: 0.1129 | Val Loss: 0.1091 | Perfect Match Accuracy: 0.16%
Epoch 0092 | Train Loss: 0.1129 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.15%
Epoch 0093 | Train Loss: 0.1130 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.16%
Epoch 0094 | Train Loss: 0.1131 | Val Loss: 0.1093 | Perfect Match Accuracy: 0.16%
Epoch 0095 | Train Loss: 0.1131 | Val Loss: 0.1093 | Perfect Match Accuracy: 0.15%
Epoch 0096 | Train Loss: 0.1130 | Val Loss: 0.1093 | Perfect Match Accuracy: 0.16%
Epoch 0097 | Train Loss: 0.1129 | Val Loss: 0.1094 | Perfect Match Accuracy: 0.16%
Epoch 0098 | Train Loss: 0.1130 | Val Loss: 0.1096 | Perfect Match Accuracy: 0.15%
Epoch 0099 | Train Loss: 0.1129 | Val Loss: 0.1094 | Perfect Match Accuracy: 0.15%
Epoch 0100 | Train Loss: 0.1128 | Val Loss: 0.1094 | Perfect Match Accuracy: 0.15%
Epoch 0101 | Train Loss: 0.1128 | Val Loss: 0.1094 | Perfect Match Accuracy: 0.15%
Epoch 0102 | Train Loss: 0.1128 | Val Loss: 0.1093 | Perfect Match Accuracy: 0.15%
Epoch 0103 | Train Loss: 0.1128 | Val Loss: 0.1095 | Perfect Match Accuracy: 0.16%
Epoch 0104 | Train Loss: 0.1129 | Val Loss: 0.1095 | Perfect Match Accuracy: 0.13%
Epoch 0105 | Train Loss: 0.1130 | Val Loss: 0.1095 | Perfect Match Accuracy: 0.14%
Epoch 0106 | Train Loss: 0.1129 | Val Loss: 0.1095 | Perfect Match Accuracy: 0.13%
Epoch 0107 | Train Loss: 0.1128 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.13%
Epoch 0108 | Train Loss: 0.1128 | Val Loss: 0.1094 | Perfect Match Accuracy: 0.12%
Epoch 0109 | Train Loss: 0.1126 | Val Loss: 0.1090 | Perfect Match Accuracy: 0.16%
Epoch 0110 | Train Loss: 0.1126 | Val Loss: 0.1091 | Perfect Match Accuracy: 0.15%
Epoch 0111 | Train Loss: 0.1127 | Val Loss: 0.1091 | Perfect Match Accuracy: 0.15%
Epoch 0112 | Train Loss: 0.1127 | Val Loss: 0.1090 | Perfect Match Accuracy: 0.17%
Epoch 0113 | Train Loss: 0.1126 | Val Loss: 0.1091 | Perfect Match Accuracy: 0.17%
Epoch 0114 | Train Loss: 0.1125 | Val Loss: 0.1089 | Perfect Match Accuracy: 0.15%
Epoch 0115 | Train Loss: 0.1124 | Val Loss: 0.1088 | Perfect Match Accuracy: 0.16%
Epoch 0116 | Train Loss: 0.1124 | Val Loss: 0.1089 | Perfect Match Accuracy: 0.16%
Epoch 0117 | Train Loss: 0.1125 | Val Loss: 0.1088 | Perfect Match Accuracy: 0.16%
Epoch 0118 | Train Loss: 0.1126 | Val Loss: 0.1088 | Perfect Match Accuracy: 0.17%
Epoch 0119 | Train Loss: 0.1127 | Val Loss: 0.1092 | Perfect Match Accuracy: 0.15%
Epoch 0120 | Train Loss: 0.1126 | Val Loss: 0.1088 | Perfect Match Accuracy: 0.17%
Epoch 0121 | Train Loss: 0.1122 | Val Loss: 0.1087 | Perfect Match Accuracy: 0.17%
Epoch 0122 | Train Loss: 0.1122 | Val Loss: 0.1086 | Perfect Match Accuracy: 0.18%
Epoch 0123 | Train Loss: 0.1121 | Val Loss: 0.1086 | Perfect Match Accuracy: 0.17%
Epoch 0124 | Train Loss: 0.1121 | Val Loss: 0.1086 | Perfect Match Accuracy: 0.19%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0125 | Train Loss: 0.1121 | Val Loss: 0.1084 | Perfect Match Accuracy: 0.19%
Epoch 0126 | Train Loss: 0.1120 | Val Loss: 0.1085 | Perfect Match Accuracy: 0.18%
Epoch 0127 | Train Loss: 0.1120 | Val Loss: 0.1083 | Perfect Match Accuracy: 0.20%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0128 | Train Loss: 0.1120 | Val Loss: 0.1084 | Perfect Match Accuracy: 0.19%
Epoch 0129 | Train Loss: 0.1118 | Val Loss: 0.1085 | Perfect Match Accuracy: 0.19%
Epoch 0130 | Train Loss: 0.1118 | Val Loss: 0.1084 | Perfect Match Accuracy: 0.20%
Epoch 0131 | Train Loss: 0.1119 | Val Loss: 0.1087 | Perfect Match Accuracy: 0.17%
Epoch 0132 | Train Loss: 0.1120 | Val Loss: 0.1088 | Perfect Match Accuracy: 0.16%
Epoch 0133 | Train Loss: 0.1121 | Val Loss: 0.1087 | Perfect Match Accuracy: 0.20%
Epoch 0134 | Train Loss: 0.1120 | Val Loss: 0.1086 | Perfect Match Accuracy: 0.19%
Epoch 0135 | Train Loss: 0.1121 | Val Loss: 0.1087 | Perfect Match Accuracy: 0.19%
Epoch 0136 | Train Loss: 0.1124 | Val Loss: 0.1089 | Perfect Match Accuracy: 0.15%
Epoch 0137 | Train Loss: 0.1124 | Val Loss: 0.1088 | Perfect Match Accuracy: 0.20%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0138 | Train Loss: 0.1123 | Val Loss: 0.1087 | Perfect Match Accuracy: 0.17%
Epoch 0139 | Train Loss: 0.1119 | Val Loss: 0.1086 | Perfect Match Accuracy: 0.20%
Epoch 0140 | Train Loss: 0.1121 | Val Loss: 0.1087 | Perfect Match Accuracy: 0.20%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0141 | Train Loss: 0.1121 | Val Loss: 0.1085 | Perfect Match Accuracy: 0.23%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0142 | Train Loss: 0.1119 | Val Loss: 0.1086 | Perfect Match Accuracy: 0.21%
Epoch 0143 | Train Loss: 0.1122 | Val Loss: 0.1086 | Perfect Match Accuracy: 0.22%
Epoch 0144 | Train Loss: 0.1124 | Val Loss: 0.1087 | Perfect Match Accuracy: 0.25%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0145 | Train Loss: 0.1125 | Val Loss: 0.1086 | Perfect Match Accuracy: 0.22%
Epoch 0146 | Train Loss: 0.1123 | Val Loss: 0.1084 | Perfect Match Accuracy: 0.22%
Epoch 0147 | Train Loss: 0.1123 | Val Loss: 0.1084 | Perfect Match Accuracy: 0.22%
Epoch 0148 | Train Loss: 0.1129 | Val Loss: 0.1087 | Perfect Match Accuracy: 0.21%
Epoch 0149 | Train Loss: 0.1133 | Val Loss: 0.1086 | Perfect Match Accuracy: 0.23%
Epoch 0150 | Train Loss: 0.1130 | Val Loss: 0.1084 | Perfect Match Accuracy: 0.23%
Epoch 0151 | Train Loss: 0.1124 | Val Loss: 0.1081 | Perfect Match Accuracy: 0.23%
Epoch 0152 | Train Loss: 0.1118 | Val Loss: 0.1080 | Perfect Match Accuracy: 0.23%
Epoch 0153 | Train Loss: 0.1120 | Val Loss: 0.1078 | Perfect Match Accuracy: 0.23%
Epoch 0154 | Train Loss: 0.1112 | Val Loss: 0.1076 | Perfect Match Accuracy: 0.25%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0155 | Train Loss: 0.1113 | Val Loss: 0.1076 | Perfect Match Accuracy: 0.23%
Epoch 0156 | Train Loss: 0.1111 | Val Loss: 0.1075 | Perfect Match Accuracy: 0.25%
Epoch 0157 | Train Loss: 0.1111 | Val Loss: 0.1077 | Perfect Match Accuracy: 0.25%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0158 | Train Loss: 0.1118 | Val Loss: 0.1079 | Perfect Match Accuracy: 0.27%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0159 | Train Loss: 0.1116 | Val Loss: 0.1076 | Perfect Match Accuracy: 0.27%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0160 | Train Loss: 0.1115 | Val Loss: 0.1075 | Perfect Match Accuracy: 0.26%
Epoch 0161 | Train Loss: 0.1117 | Val Loss: 0.1078 | Perfect Match Accuracy: 0.25%
Epoch 0162 | Train Loss: 0.1119 | Val Loss: 0.1075 | Perfect Match Accuracy: 0.29%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0163 | Train Loss: 0.1121 | Val Loss: 0.1079 | Perfect Match Accuracy: 0.27%
Epoch 0164 | Train Loss: 0.1125 | Val Loss: 0.1081 | Perfect Match Accuracy: 0.22%
Epoch 0165 | Train Loss: 0.1126 | Val Loss: 0.1083 | Perfect Match Accuracy: 0.25%
Epoch 0166 | Train Loss: 0.1127 | Val Loss: 0.1081 | Perfect Match Accuracy: 0.26%
Epoch 0167 | Train Loss: 0.1119 | Val Loss: 0.1075 | Perfect Match Accuracy: 0.26%
Epoch 0168 | Train Loss: 0.1118 | Val Loss: 0.1078 | Perfect Match Accuracy: 0.25%
Epoch 0169 | Train Loss: 0.1128 | Val Loss: 0.1083 | Perfect Match Accuracy: 0.24%
Epoch 0170 | Train Loss: 0.1129 | Val Loss: 0.1079 | Perfect Match Accuracy: 0.24%
Epoch 0171 | Train Loss: 0.1122 | Val Loss: 0.1085 | Perfect Match Accuracy: 0.27%
Epoch 0172 | Train Loss: 0.1122 | Val Loss: 0.1075 | Perfect Match Accuracy: 0.27%
Epoch 0173 | Train Loss: 0.1113 | Val Loss: 0.1069 | Perfect Match Accuracy: 0.31%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0174 | Train Loss: 0.1108 | Val Loss: 0.1070 | Perfect Match Accuracy: 0.32%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0175 | Train Loss: 0.1107 | Val Loss: 0.1064 | Perfect Match Accuracy: 0.34%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0176 | Train Loss: 0.1104 | Val Loss: 0.1056 | Perfect Match Accuracy: 0.33%
Epoch 0177 | Train Loss: 0.1103 | Val Loss: 0.1056 | Perfect Match Accuracy: 0.30%
Epoch 0178 | Train Loss: 0.1098 | Val Loss: 0.1053 | Perfect Match Accuracy: 0.35%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0179 | Train Loss: 0.1097 | Val Loss: 0.1054 | Perfect Match Accuracy: 0.34%
Epoch 0180 | Train Loss: 0.1104 | Val Loss: 0.1055 | Perfect Match Accuracy: 0.32%
Epoch 0181 | Train Loss: 0.1101 | Val Loss: 0.1052 | Perfect Match Accuracy: 0.34%
Epoch 0182 | Train Loss: 0.1099 | Val Loss: 0.1051 | Perfect Match Accuracy: 0.36%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0183 | Train Loss: 0.1094 | Val Loss: 0.1048 | Perfect Match Accuracy: 0.36%
Epoch 0184 | Train Loss: 0.1090 | Val Loss: 0.1046 | Perfect Match Accuracy: 0.36%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0185 | Train Loss: 0.1089 | Val Loss: 0.1051 | Perfect Match Accuracy: 0.34%
Epoch 0186 | Train Loss: 0.1094 | Val Loss: 0.1048 | Perfect Match Accuracy: 0.36%
Epoch 0187 | Train Loss: 0.1087 | Val Loss: 0.1045 | Perfect Match Accuracy: 0.39%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0188 | Train Loss: 0.1087 | Val Loss: 0.1044 | Perfect Match Accuracy: 0.40%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0189 | Train Loss: 0.1088 | Val Loss: 0.1046 | Perfect Match Accuracy: 0.41%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0190 | Train Loss: 0.1090 | Val Loss: 0.1044 | Perfect Match Accuracy: 0.42%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0191 | Train Loss: 0.1088 | Val Loss: 0.1039 | Perfect Match Accuracy: 0.42%
Epoch 0192 | Train Loss: 0.1079 | Val Loss: 0.1036 | Perfect Match Accuracy: 0.45%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0193 | Train Loss: 0.1076 | Val Loss: 0.1032 | Perfect Match Accuracy: 0.45%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0194 | Train Loss: 0.1072 | Val Loss: 0.1034 | Perfect Match Accuracy: 0.42%
Epoch 0195 | Train Loss: 0.1070 | Val Loss: 0.1030 | Perfect Match Accuracy: 0.39%
Epoch 0196 | Train Loss: 0.1068 | Val Loss: 0.1030 | Perfect Match Accuracy: 0.43%
Epoch 0197 | Train Loss: 0.1065 | Val Loss: 0.1030 | Perfect Match Accuracy: 0.42%
Epoch 0198 | Train Loss: 0.1063 | Val Loss: 0.1025 | Perfect Match Accuracy: 0.44%
Epoch 0199 | Train Loss: 0.1063 | Val Loss: 0.1025 | Perfect Match Accuracy: 0.43%
Epoch 0200 | Train Loss: 0.1060 | Val Loss: 0.1025 | Perfect Match Accuracy: 0.47%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0201 | Train Loss: 0.1060 | Val Loss: 0.1024 | Perfect Match Accuracy: 0.46%
Epoch 0202 | Train Loss: 0.1061 | Val Loss: 0.1026 | Perfect Match Accuracy: 0.45%
Epoch 0203 | Train Loss: 0.1061 | Val Loss: 0.1024 | Perfect Match Accuracy: 0.44%
Epoch 0204 | Train Loss: 0.1063 | Val Loss: 0.1028 | Perfect Match Accuracy: 0.44%
Epoch 0205 | Train Loss: 0.1065 | Val Loss: 0.1029 | Perfect Match Accuracy: 0.43%
Epoch 0206 | Train Loss: 0.1063 | Val Loss: 0.1026 | Perfect Match Accuracy: 0.46%
Epoch 0207 | Train Loss: 0.1062 | Val Loss: 0.1022 | Perfect Match Accuracy: 0.43%
Epoch 0208 | Train Loss: 0.1066 | Val Loss: 0.1031 | Perfect Match Accuracy: 0.45%
Epoch 0209 | Train Loss: 0.1068 | Val Loss: 0.1036 | Perfect Match Accuracy: 0.43%
Epoch 0210 | Train Loss: 0.1066 | Val Loss: 0.1029 | Perfect Match Accuracy: 0.44%
Epoch 0211 | Train Loss: 0.1064 | Val Loss: 0.1023 | Perfect Match Accuracy: 0.46%
Epoch 0212 | Train Loss: 0.1064 | Val Loss: 0.1040 | Perfect Match Accuracy: 0.39%
Epoch 0213 | Train Loss: 0.1062 | Val Loss: 0.1027 | Perfect Match Accuracy: 0.48%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0214 | Train Loss: 0.1071 | Val Loss: 0.1024 | Perfect Match Accuracy: 0.44%
Epoch 0215 | Train Loss: 0.1088 | Val Loss: 0.1052 | Perfect Match Accuracy: 0.40%
Epoch 0216 | Train Loss: 0.1118 | Val Loss: 0.1057 | Perfect Match Accuracy: 0.41%
Epoch 0217 | Train Loss: 0.1232 | Val Loss: 0.1131 | Perfect Match Accuracy: 0.24%
Epoch 0218 | Train Loss: 0.1380 | Val Loss: 0.1249 | Perfect Match Accuracy: 0.13%
Epoch 0219 | Train Loss: 0.1393 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.18%
Epoch 0220 | Train Loss: 0.1360 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.20%
Epoch 0221 | Train Loss: 0.1177 | Val Loss: 0.1067 | Perfect Match Accuracy: 0.30%
Epoch 0222 | Train Loss: 0.1114 | Val Loss: 0.1070 | Perfect Match Accuracy: 0.35%
Epoch 0223 | Train Loss: 0.1116 | Val Loss: 0.1045 | Perfect Match Accuracy: 0.35%
Epoch 0224 | Train Loss: 0.1100 | Val Loss: 0.1047 | Perfect Match Accuracy: 0.37%
Epoch 0225 | Train Loss: 0.1094 | Val Loss: 0.1043 | Perfect Match Accuracy: 0.38%
Epoch 0226 | Train Loss: 0.1090 | Val Loss: 0.1035 | Perfect Match Accuracy: 0.41%
Epoch 0227 | Train Loss: 0.1077 | Val Loss: 0.1030 | Perfect Match Accuracy: 0.43%
Epoch 0228 | Train Loss: 0.1076 | Val Loss: 0.1031 | Perfect Match Accuracy: 0.41%
Epoch 0229 | Train Loss: 0.1098 | Val Loss: 0.1038 | Perfect Match Accuracy: 0.40%
Epoch 0230 | Train Loss: 0.1111 | Val Loss: 0.1046 | Perfect Match Accuracy: 0.38%
Epoch 0231 | Train Loss: 0.1112 | Val Loss: 0.1031 | Perfect Match Accuracy: 0.40%
Epoch 0232 | Train Loss: 0.1100 | Val Loss: 0.1039 | Perfect Match Accuracy: 0.39%
Epoch 0233 | Train Loss: 0.1100 | Val Loss: 0.1046 | Perfect Match Accuracy: 0.42%
Epoch 0234 | Train Loss: 0.1098 | Val Loss: 0.1041 | Perfect Match Accuracy: 0.40%
Epoch 0235 | Train Loss: 0.1094 | Val Loss: 0.1033 | Perfect Match Accuracy: 0.44%
Epoch 0236 | Train Loss: 0.1097 | Val Loss: 0.1034 | Perfect Match Accuracy: 0.44%
Epoch 0237 | Train Loss: 0.1089 | Val Loss: 0.1038 | Perfect Match Accuracy: 0.44%
Epoch 0238 | Train Loss: 0.1087 | Val Loss: 0.1029 | Perfect Match Accuracy: 0.47%
Epoch 0239 | Train Loss: 0.1084 | Val Loss: 0.1030 | Perfect Match Accuracy: 0.45%
Epoch 0240 | Train Loss: 0.1087 | Val Loss: 0.1029 | Perfect Match Accuracy: 0.46%
Epoch 0241 | Train Loss: 0.1087 | Val Loss: 0.1026 | Perfect Match Accuracy: 0.44%
Epoch 0242 | Train Loss: 0.1082 | Val Loss: 0.1017 | Perfect Match Accuracy: 0.49%
  ---  New best perfrct match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0243 | Train Loss: 0.1079 | Val Loss: 0.1016 | Perfect Match Accuracy: 0.49%
Epoch 0244 | Train Loss: 0.1095 | Val Loss: 0.1020 | Perfect Match Accuracy: 0.47%
Epoch 0245 | Train Loss: 0.1094 | Val Loss: 0.1048 | Perfect Match Accuracy: 0.45%
Epoch 0246 | Train Loss: 0.1101 | Val Loss: 0.1039 | Perfect Match Accuracy: 0.44%
Epoch 0247 | Train Loss: 0.1101 | Val Loss: 0.1042 | Perfect Match Accuracy: 0.49%
Epoch 0248 | Train Loss: 0.1112 | Val Loss: 0.1030 | Perfect Match Accuracy: 0.45%
Epoch 0249 | Train Loss: 0.1115 | Val Loss: 0.1047 | Perfect Match Accuracy: 0.42%
Epoch 0250 | Train Loss: 0.1129 | Val Loss: 0.1071 | Perfect Match Accuracy: 0.40%
Epoch 0251 | Train Loss: 0.1132 | Val Loss: 0.1048 | Perfect Match Accuracy: 0.42%
Epoch 0252 | Train Loss: 0.1118 | Val Loss: 0.1032 | Perfect Match Accuracy: 0.45%
Epoch 0253 | Train Loss: 0.1105 | Val Loss: 0.1034 | Perfect Match Accuracy: 0.46%
Epoch 0254 | Train Loss: 0.1108 | Val Loss: 0.1038 | Perfect Match Accuracy: 0.44%
Epoch 0255 | Train Loss: 0.1116 | Val Loss: 0.1051 | Perfect Match Accuracy: 0.45%
Epoch 0256 | Train Loss: 0.1117 | Val Loss: 0.1040 | Perfect Match Accuracy: 0.45%
Epoch 0257 | Train Loss: 0.1123 | Val Loss: 0.1054 | Perfect Match Accuracy: 0.46%
Epoch 0258 | Train Loss: 0.1134 | Val Loss: 0.1051 | Perfect Match Accuracy: 0.46%
Epoch 0259 | Train Loss: 0.1136 | Val Loss: 0.1048 | Perfect Match Accuracy: 0.47%
Epoch 0260 | Train Loss: 0.1152 | Val Loss: 0.1057 | Perfect Match Accuracy: 0.46%
Epoch 0261 | Train Loss: 0.1160 | Val Loss: 0.1060 | Perfect Match Accuracy: 0.45%
Epoch 0262 | Train Loss: 0.1163 | Val Loss: 0.1061 | Perfect Match Accuracy: 0.46%
Epoch 0263 | Train Loss: 0.1181 | Val Loss: 0.1066 | Perfect Match Accuracy: 0.47%
Epoch 0264 | Train Loss: 0.1201 | Val Loss: 0.1094 | Perfect Match Accuracy: 0.42%
Epoch 0265 | Train Loss: 0.1222 | Val Loss: 0.1101 | Perfect Match Accuracy: 0.43%
Epoch 0266 | Train Loss: 0.1249 | Val Loss: 0.1117 | Perfect Match Accuracy: 0.38%
Epoch 0267 | Train Loss: 0.1273 | Val Loss: 0.1117 | Perfect Match Accuracy: 0.38%
Epoch 0268 | Train Loss: 0.1293 | Val Loss: 0.1113 | Perfect Match Accuracy: 0.40%
Epoch 0269 | Train Loss: 0.1319 | Val Loss: 0.1145 | Perfect Match Accuracy: 0.35%
Epoch 0270 | Train Loss: 0.1349 | Val Loss: 0.1180 | Perfect Match Accuracy: 0.35%
Epoch 0271 | Train Loss: 0.1380 | Val Loss: 0.1202 | Perfect Match Accuracy: 0.34%
Epoch 0272 | Train Loss: 0.1444 | Val Loss: 0.1223 | Perfect Match Accuracy: 0.35%
Epoch 0273 | Train Loss: 0.1484 | Val Loss: 0.1237 | Perfect Match Accuracy: 0.33%
Epoch 0274 | Train Loss: 0.1539 | Val Loss: 0.1263 | Perfect Match Accuracy: 0.33%
Epoch 0275 | Train Loss: 0.1580 | Val Loss: 0.1402 | Perfect Match Accuracy: 0.30%
Epoch 0276 | Train Loss: 0.1681 | Val Loss: 0.1334 | Perfect Match Accuracy: 0.27%
Epoch 0277 | Train Loss: 0.1704 | Val Loss: 0.1374 | Perfect Match Accuracy: 0.27%
Epoch 0278 | Train Loss: 0.1748 | Val Loss: 0.1370 | Perfect Match Accuracy: 0.27%
Epoch 0279 | Train Loss: 0.1795 | Val Loss: 0.1362 | Perfect Match Accuracy: 0.25%
Epoch 0280 | Train Loss: 0.1815 | Val Loss: 0.1357 | Perfect Match Accuracy: 0.24%
Epoch 0281 | Train Loss: 0.1857 | Val Loss: 0.1399 | Perfect Match Accuracy: 0.22%
Epoch 0282 | Train Loss: 0.1867 | Val Loss: 0.1393 | Perfect Match Accuracy: 0.22%
Epoch 0283 | Train Loss: 0.1899 | Val Loss: 0.1394 | Perfect Match Accuracy: 0.23%
Epoch 0284 | Train Loss: 0.1919 | Val Loss: 0.1463 | Perfect Match Accuracy: 0.24%
Epoch 0285 | Train Loss: 0.1999 | Val Loss: 0.1487 | Perfect Match Accuracy: 0.21%
Epoch 0286 | Train Loss: 0.1979 | Val Loss: 0.1442 | Perfect Match Accuracy: 0.24%
Epoch 0287 | Train Loss: 0.1966 | Val Loss: 0.1445 | Perfect Match Accuracy: 0.22%
Epoch 0288 | Train Loss: 0.1999 | Val Loss: 0.1456 | Perfect Match Accuracy: 0.21%
Epoch 0289 | Train Loss: 0.2010 | Val Loss: 0.1464 | Perfect Match Accuracy: 0.21%
Epoch 0290 | Train Loss: 0.1998 | Val Loss: 0.1476 | Perfect Match Accuracy: 0.21%
Epoch 0291 | Train Loss: 0.2018 | Val Loss: 0.1496 | Perfect Match Accuracy: 0.22%
Epoch 0292 | Train Loss: 0.2039 | Val Loss: 0.1488 | Perfect Match Accuracy: 0.20%
Epoch 0293 | Train Loss: 0.2029 | Val Loss: 0.1618 | Perfect Match Accuracy: 0.20%
Epoch 0294 | Train Loss: 0.2027 | Val Loss: 0.1499 | Perfect Match Accuracy: 0.21%
Epoch 0295 | Train Loss: 0.1995 | Val Loss: 0.1458 | Perfect Match Accuracy: 0.21%
Epoch 0296 | Train Loss: 0.1983 | Val Loss: 0.1494 | Perfect Match Accuracy: 0.21%
Epoch 0297 | Train Loss: 0.1984 | Val Loss: 0.1476 | Perfect Match Accuracy: 0.20%
Epoch 0298 | Train Loss: 0.1988 | Val Loss: 0.1488 | Perfect Match Accuracy: 0.19%
Epoch 0299 | Train Loss: 0.1993 | Val Loss: 0.1451 | Perfect Match Accuracy: 0.19%
Epoch 0300 | Train Loss: 0.1989 | Val Loss: 0.1499 | Perfect Match Accuracy: 0.21%
Epoch 0301 | Train Loss: 0.1999 | Val Loss: 0.1462 | Perfect Match Accuracy: 0.21%
Epoch 0302 | Train Loss: 0.1983 | Val Loss: 0.1487 | Perfect Match Accuracy: 0.20%
Epoch 0303 | Train Loss: 0.1984 | Val Loss: 0.1493 | Perfect Match Accuracy: 0.20%
Epoch 0304 | Train Loss: 0.1994 | Val Loss: 0.1470 | Perfect Match Accuracy: 0.18%
Epoch 0305 | Train Loss: 0.1965 | Val Loss: 0.1465 | Perfect Match Accuracy: 0.19%
Epoch 0306 | Train Loss: 0.1968 | Val Loss: 0.1446 | Perfect Match Accuracy: 0.19%
Epoch 0307 | Train Loss: 0.1945 | Val Loss: 0.1455 | Perfect Match Accuracy: 0.19%
Epoch 0308 | Train Loss: 0.1946 | Val Loss: 0.1434 | Perfect Match Accuracy: 0.20%
Epoch 0309 | Train Loss: 0.1938 | Val Loss: 0.1457 | Perfect Match Accuracy: 0.20%
Epoch 0310 | Train Loss: 0.1951 | Val Loss: 0.1462 | Perfect Match Accuracy: 0.20%
Epoch 0311 | Train Loss: 0.1945 | Val Loss: 0.1436 | Perfect Match Accuracy: 0.18%
Epoch 0312 | Train Loss: 0.1933 | Val Loss: 0.1447 | Perfect Match Accuracy: 0.18%
Epoch 0313 | Train Loss: 0.1933 | Val Loss: 0.1459 | Perfect Match Accuracy: 0.19%
Epoch 0314 | Train Loss: 0.1934 | Val Loss: 0.1438 | Perfect Match Accuracy: 0.18%
Epoch 0315 | Train Loss: 0.1909 | Val Loss: 0.1599 | Perfect Match Accuracy: 0.20%
Epoch 0316 | Train Loss: 0.1886 | Val Loss: 0.1414 | Perfect Match Accuracy: 0.19%
Epoch 0317 | Train Loss: 0.1885 | Val Loss: 0.1432 | Perfect Match Accuracy: 0.19%
Epoch 0318 | Train Loss: 0.1901 | Val Loss: 0.1424 | Perfect Match Accuracy: 0.18%
Epoch 0319 | Train Loss: 0.1889 | Val Loss: 0.1543 | Perfect Match Accuracy: 0.18%
Epoch 0320 | Train Loss: 0.1894 | Val Loss: 0.1405 | Perfect Match Accuracy: 0.19%
Epoch 0321 | Train Loss: 0.1869 | Val Loss: 0.1424 | Perfect Match Accuracy: 0.19%
Epoch 0322 | Train Loss: 0.1902 | Val Loss: 0.1399 | Perfect Match Accuracy: 0.20%
Epoch 0323 | Train Loss: 0.1864 | Val Loss: 0.1416 | Perfect Match Accuracy: 0.19%
Epoch 0324 | Train Loss: 0.1841 | Val Loss: 0.1407 | Perfect Match Accuracy: 0.18%
Epoch 0325 | Train Loss: 0.1828 | Val Loss: 0.1384 | Perfect Match Accuracy: 0.18%
Epoch 0326 | Train Loss: 0.1819 | Val Loss: 0.1417 | Perfect Match Accuracy: 0.19%
Epoch 0327 | Train Loss: 0.1803 | Val Loss: 0.1514 | Perfect Match Accuracy: 0.19%
Epoch 0328 | Train Loss: 0.1797 | Val Loss: 0.1412 | Perfect Match Accuracy: 0.20%
Epoch 0329 | Train Loss: 0.1787 | Val Loss: 0.1387 | Perfect Match Accuracy: 0.18%
Epoch 0330 | Train Loss: 0.1765 | Val Loss: 0.1380 | Perfect Match Accuracy: 0.19%
Epoch 0331 | Train Loss: 0.1745 | Val Loss: 0.1358 | Perfect Match Accuracy: 0.19%
Epoch 0332 | Train Loss: 0.1729 | Val Loss: 0.1361 | Perfect Match Accuracy: 0.16%
Epoch 0333 | Train Loss: 0.1710 | Val Loss: 0.1329 | Perfect Match Accuracy: 0.17%
Epoch 0334 | Train Loss: 0.1659 | Val Loss: 0.1303 | Perfect Match Accuracy: 0.18%
Epoch 0335 | Train Loss: 0.1617 | Val Loss: 0.1275 | Perfect Match Accuracy: 0.19%
Epoch 0336 | Train Loss: 0.1589 | Val Loss: 0.1259 | Perfect Match Accuracy: 0.20%
Epoch 0337 | Train Loss: 0.1553 | Val Loss: 0.1241 | Perfect Match Accuracy: 0.20%
Epoch 0338 | Train Loss: 0.1528 | Val Loss: 0.1258 | Perfect Match Accuracy: 0.22%
Epoch 0339 | Train Loss: 0.1486 | Val Loss: 0.1219 | Perfect Match Accuracy: 0.24%
Epoch 0340 | Train Loss: 0.1453 | Val Loss: 0.1206 | Perfect Match Accuracy: 0.25%
Epoch 0341 | Train Loss: 0.1423 | Val Loss: 0.1194 | Perfect Match Accuracy: 0.23%
Epoch 0342 | Train Loss: 0.1405 | Val Loss: 0.1184 | Perfect Match Accuracy: 0.26%
Epoch 0343 | Train Loss: 0.1386 | Val Loss: 0.1178 | Perfect Match Accuracy: 0.29%
Epoch 0344 | Train Loss: 0.1369 | Val Loss: 0.1175 | Perfect Match Accuracy: 0.29%
Epoch 0345 | Train Loss: 0.1361 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.30%
Epoch 0346 | Train Loss: 0.1348 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.29%
Epoch 0347 | Train Loss: 0.1337 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.30%
Epoch 0348 | Train Loss: 0.1326 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.31%
Epoch 0349 | Train Loss: 0.1331 | Val Loss: 0.1151 | Perfect Match Accuracy: 0.29%
Epoch 0350 | Train Loss: 0.1329 | Val Loss: 0.1148 | Perfect Match Accuracy: 0.31%
Epoch 0351 | Train Loss: 0.1323 | Val Loss: 0.1146 | Perfect Match Accuracy: 0.30%
Epoch 0352 | Train Loss: 0.1326 | Val Loss: 0.1145 | Perfect Match Accuracy: 0.30%
Epoch 0353 | Train Loss: 0.1329 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.32%
Epoch 0354 | Train Loss: 0.1333 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.30%
Epoch 0355 | Train Loss: 0.1334 | Val Loss: 0.1150 | Perfect Match Accuracy: 0.30%
Epoch 0356 | Train Loss: 0.1342 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.28%
Epoch 0357 | Train Loss: 0.1336 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.29%
Epoch 0358 | Train Loss: 0.1349 | Val Loss: 0.1173 | Perfect Match Accuracy: 0.30%
Epoch 0359 | Train Loss: 0.1354 | Val Loss: 0.1173 | Perfect Match Accuracy: 0.30%
Epoch 0360 | Train Loss: 0.1352 | Val Loss: 0.1173 | Perfect Match Accuracy: 0.31%
Epoch 0361 | Train Loss: 0.1349 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.32%
Epoch 0362 | Train Loss: 0.1336 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.29%
Epoch 0363 | Train Loss: 0.1335 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.27%
Epoch 0364 | Train Loss: 0.1338 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.31%
Epoch 0365 | Train Loss: 0.1346 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.33%
Epoch 0366 | Train Loss: 0.1351 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.31%
Epoch 0367 | Train Loss: 0.1342 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.30%
Epoch 0368 | Train Loss: 0.1342 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.31%
Epoch 0369 | Train Loss: 0.1338 | Val Loss: 0.1185 | Perfect Match Accuracy: 0.29%
Epoch 0370 | Train Loss: 0.1315 | Val Loss: 0.1165 | Perfect Match Accuracy: 0.31%
Epoch 0371 | Train Loss: 0.1328 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.29%
Epoch 0372 | Train Loss: 0.1337 | Val Loss: 0.1145 | Perfect Match Accuracy: 0.32%
Epoch 0373 | Train Loss: 0.1335 | Val Loss: 0.1148 | Perfect Match Accuracy: 0.34%
Epoch 0374 | Train Loss: 0.1345 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.34%
Epoch 0375 | Train Loss: 0.1344 | Val Loss: 0.1145 | Perfect Match Accuracy: 0.34%
Epoch 0376 | Train Loss: 0.1340 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.33%
Epoch 0377 | Train Loss: 0.1328 | Val Loss: 0.1149 | Perfect Match Accuracy: 0.35%
Epoch 0378 | Train Loss: 0.1323 | Val Loss: 0.1147 | Perfect Match Accuracy: 0.33%
Epoch 0379 | Train Loss: 0.1319 | Val Loss: 0.1146 | Perfect Match Accuracy: 0.34%
Epoch 0380 | Train Loss: 0.1319 | Val Loss: 0.1136 | Perfect Match Accuracy: 0.33%
Epoch 0381 | Train Loss: 0.1311 | Val Loss: 0.1137 | Perfect Match Accuracy: 0.31%
Epoch 0382 | Train Loss: 0.1312 | Val Loss: 0.1145 | Perfect Match Accuracy: 0.36%
Epoch 0383 | Train Loss: 0.1304 | Val Loss: 0.1139 | Perfect Match Accuracy: 0.34%
Epoch 0384 | Train Loss: 0.1299 | Val Loss: 0.1133 | Perfect Match Accuracy: 0.33%
Epoch 0385 | Train Loss: 0.1298 | Val Loss: 0.1137 | Perfect Match Accuracy: 0.34%
Epoch 0386 | Train Loss: 0.1296 | Val Loss: 0.1132 | Perfect Match Accuracy: 0.35%
Epoch 0387 | Train Loss: 0.1290 | Val Loss: 0.1132 | Perfect Match Accuracy: 0.37%
Epoch 0388 | Train Loss: 0.1290 | Val Loss: 0.1129 | Perfect Match Accuracy: 0.36%
Epoch 0389 | Train Loss: 0.1286 | Val Loss: 0.1116 | Perfect Match Accuracy: 0.40%
Epoch 0390 | Train Loss: 0.1292 | Val Loss: 0.1125 | Perfect Match Accuracy: 0.38%
Epoch 0391 | Train Loss: 0.1283 | Val Loss: 0.1127 | Perfect Match Accuracy: 0.36%
Epoch 0392 | Train Loss: 0.1285 | Val Loss: 0.1127 | Perfect Match Accuracy: 0.36%
Epoch 0393 | Train Loss: 0.1286 | Val Loss: 0.1123 | Perfect Match Accuracy: 0.40%
Epoch 0394 | Train Loss: 0.1286 | Val Loss: 0.1132 | Perfect Match Accuracy: 0.39%
Epoch 0395 | Train Loss: 0.1283 | Val Loss: 0.1124 | Perfect Match Accuracy: 0.39%
Epoch 0396 | Train Loss: 0.1284 | Val Loss: 0.1120 | Perfect Match Accuracy: 0.40%
Epoch 0397 | Train Loss: 0.1283 | Val Loss: 0.1118 | Perfect Match Accuracy: 0.38%
Epoch 0398 | Train Loss: 0.1284 | Val Loss: 0.1114 | Perfect Match Accuracy: 0.38%
Epoch 0399 | Train Loss: 0.1297 | Val Loss: 0.1120 | Perfect Match Accuracy: 0.41%
Epoch 0400 | Train Loss: 0.1290 | Val Loss: 0.1115 | Perfect Match Accuracy: 0.39%
Epoch 0401 | Train Loss: 0.1288 | Val Loss: 0.1122 | Perfect Match Accuracy: 0.39%
Epoch 0402 | Train Loss: 0.1284 | Val Loss: 0.1134 | Perfect Match Accuracy: 0.39%
Epoch 0403 | Train Loss: 0.1295 | Val Loss: 0.1119 | Perfect Match Accuracy: 0.41%
Epoch 0404 | Train Loss: 0.1294 | Val Loss: 0.1124 | Perfect Match Accuracy: 0.38%
Epoch 0405 | Train Loss: 0.1306 | Val Loss: 0.1125 | Perfect Match Accuracy: 0.39%
Epoch 0406 | Train Loss: 0.1310 | Val Loss: 0.1127 | Perfect Match Accuracy: 0.36%
Epoch 0407 | Train Loss: 0.1307 | Val Loss: 0.1122 | Perfect Match Accuracy: 0.38%
Epoch 0408 | Train Loss: 0.1307 | Val Loss: 0.1116 | Perfect Match Accuracy: 0.40%
Epoch 0409 | Train Loss: 0.1299 | Val Loss: 0.1116 | Perfect Match Accuracy: 0.40%
Epoch 0410 | Train Loss: 0.1302 | Val Loss: 0.1122 | Perfect Match Accuracy: 0.38%
Epoch 0411 | Train Loss: 0.1309 | Val Loss: 0.1116 | Perfect Match Accuracy: 0.37%
Epoch 0412 | Train Loss: 0.1311 | Val Loss: 0.1125 | Perfect Match Accuracy: 0.39%
Epoch 0413 | Train Loss: 0.1313 | Val Loss: 0.1118 | Perfect Match Accuracy: 0.41%
Epoch 0414 | Train Loss: 0.1315 | Val Loss: 0.1119 | Perfect Match Accuracy: 0.41%
Epoch 0415 | Train Loss: 0.1315 | Val Loss: 0.1121 | Perfect Match Accuracy: 0.41%
Epoch 0416 | Train Loss: 0.1310 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.36%
Epoch 0417 | Train Loss: 0.1307 | Val Loss: 0.1126 | Perfect Match Accuracy: 0.37%
Epoch 0418 | Train Loss: 0.1303 | Val Loss: 0.1121 | Perfect Match Accuracy: 0.36%
Epoch 0419 | Train Loss: 0.1297 | Val Loss: 0.1113 | Perfect Match Accuracy: 0.40%
Epoch 0420 | Train Loss: 0.1300 | Val Loss: 0.1122 | Perfect Match Accuracy: 0.39%
Epoch 0421 | Train Loss: 0.1310 | Val Loss: 0.1118 | Perfect Match Accuracy: 0.39%
Epoch 0422 | Train Loss: 0.1314 | Val Loss: 0.1132 | Perfect Match Accuracy: 0.35%
Epoch 0423 | Train Loss: 0.1306 | Val Loss: 0.1122 | Perfect Match Accuracy: 0.38%
Epoch 0424 | Train Loss: 0.1309 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.39%
Epoch 0425 | Train Loss: 0.1319 | Val Loss: 0.1119 | Perfect Match Accuracy: 0.36%
Epoch 0426 | Train Loss: 0.1315 | Val Loss: 0.1116 | Perfect Match Accuracy: 0.38%
Epoch 0427 | Train Loss: 0.1323 | Val Loss: 0.1121 | Perfect Match Accuracy: 0.41%
Epoch 0428 | Train Loss: 0.1324 | Val Loss: 0.1116 | Perfect Match Accuracy: 0.39%
Epoch 0429 | Train Loss: 0.1331 | Val Loss: 0.1119 | Perfect Match Accuracy: 0.39%
Epoch 0430 | Train Loss: 0.1334 | Val Loss: 0.1121 | Perfect Match Accuracy: 0.37%
Epoch 0431 | Train Loss: 0.1333 | Val Loss: 0.1114 | Perfect Match Accuracy: 0.39%
Epoch 0432 | Train Loss: 0.1343 | Val Loss: 0.1108 | Perfect Match Accuracy: 0.43%
Epoch 0433 | Train Loss: 0.1344 | Val Loss: 0.1114 | Perfect Match Accuracy: 0.39%
Epoch 0434 | Train Loss: 0.1350 | Val Loss: 0.1113 | Perfect Match Accuracy: 0.39%
Epoch 0435 | Train Loss: 0.1349 | Val Loss: 0.1111 | Perfect Match Accuracy: 0.40%
Epoch 0436 | Train Loss: 0.1355 | Val Loss: 0.1114 | Perfect Match Accuracy: 0.41%
Epoch 0437 | Train Loss: 0.1368 | Val Loss: 0.1119 | Perfect Match Accuracy: 0.43%
Epoch 0438 | Train Loss: 0.1371 | Val Loss: 0.1123 | Perfect Match Accuracy: 0.42%
Epoch 0439 | Train Loss: 0.1378 | Val Loss: 0.1127 | Perfect Match Accuracy: 0.40%
Epoch 0440 | Train Loss: 0.1394 | Val Loss: 0.1125 | Perfect Match Accuracy: 0.43%
Epoch 0441 | Train Loss: 0.1413 | Val Loss: 0.1125 | Perfect Match Accuracy: 0.40%
Epoch 0442 | Train Loss: 0.1408 | Val Loss: 0.1128 | Perfect Match Accuracy: 0.41%
Epoch 0443 | Train Loss: 0.1437 | Val Loss: 0.1132 | Perfect Match Accuracy: 0.39%
Epoch 0444 | Train Loss: 0.1467 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.38%
Epoch 0445 | Train Loss: 0.1550 | Val Loss: 0.1189 | Perfect Match Accuracy: 0.35%
Epoch 0446 | Train Loss: 0.1577 | Val Loss: 0.1191 | Perfect Match Accuracy: 0.36%
Epoch 0447 | Train Loss: 0.1580 | Val Loss: 0.1181 | Perfect Match Accuracy: 0.36%
Epoch 0448 | Train Loss: 0.1584 | Val Loss: 0.1180 | Perfect Match Accuracy: 0.34%
Epoch 0449 | Train Loss: 0.1600 | Val Loss: 0.1174 | Perfect Match Accuracy: 0.35%
Epoch 0450 | Train Loss: 0.1604 | Val Loss: 0.1174 | Perfect Match Accuracy: 0.36%
Epoch 0451 | Train Loss: 0.1603 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.34%
Epoch 0452 | Train Loss: 0.1639 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.33%
Epoch 0453 | Train Loss: 0.1640 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.36%
Epoch 0454 | Train Loss: 0.1653 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.32%
Epoch 0455 | Train Loss: 0.1649 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.34%
Epoch 0456 | Train Loss: 0.1632 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.35%
Epoch 0457 | Train Loss: 0.1642 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.33%
Epoch 0458 | Train Loss: 0.1637 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.33%
Epoch 0459 | Train Loss: 0.1639 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.35%
Epoch 0460 | Train Loss: 0.1635 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.36%
Epoch 0461 | Train Loss: 0.1637 | Val Loss: 0.1177 | Perfect Match Accuracy: 0.40%
Epoch 0462 | Train Loss: 0.1627 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.34%
Epoch 0463 | Train Loss: 0.1627 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.37%
Epoch 0464 | Train Loss: 0.1622 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.37%
Epoch 0465 | Train Loss: 0.1619 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.37%
Epoch 0466 | Train Loss: 0.1610 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.35%
Epoch 0467 | Train Loss: 0.1598 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.37%
Epoch 0468 | Train Loss: 0.1601 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.39%
Epoch 0469 | Train Loss: 0.1620 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.38%
Epoch 0470 | Train Loss: 0.1635 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.36%
Epoch 0471 | Train Loss: 0.1621 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.40%
Epoch 0472 | Train Loss: 0.1621 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.37%
Epoch 0473 | Train Loss: 0.1612 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.40%
Epoch 0474 | Train Loss: 0.1624 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.39%
Epoch 0475 | Train Loss: 0.1629 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.40%
Epoch 0476 | Train Loss: 0.1636 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.40%
Epoch 0477 | Train Loss: 0.1640 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.39%
Epoch 0478 | Train Loss: 0.1648 | Val Loss: 0.1179 | Perfect Match Accuracy: 0.38%
Epoch 0479 | Train Loss: 0.1647 | Val Loss: 0.1174 | Perfect Match Accuracy: 0.40%
Epoch 0480 | Train Loss: 0.1646 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.41%
Epoch 0481 | Train Loss: 0.1634 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.41%
Epoch 0482 | Train Loss: 0.1629 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.40%
Epoch 0483 | Train Loss: 0.1632 | Val Loss: 0.1175 | Perfect Match Accuracy: 0.38%
Epoch 0484 | Train Loss: 0.1629 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.41%
Epoch 0485 | Train Loss: 0.1630 | Val Loss: 0.1176 | Perfect Match Accuracy: 0.40%
Epoch 0486 | Train Loss: 0.1642 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.38%
Epoch 0487 | Train Loss: 0.1647 | Val Loss: 0.1176 | Perfect Match Accuracy: 0.38%
Epoch 0488 | Train Loss: 0.1661 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.40%
Epoch 0489 | Train Loss: 0.1669 | Val Loss: 0.1177 | Perfect Match Accuracy: 0.38%
Epoch 0490 | Train Loss: 0.1673 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.38%
Epoch 0491 | Train Loss: 0.1670 | Val Loss: 0.1185 | Perfect Match Accuracy: 0.36%
Epoch 0492 | Train Loss: 0.1677 | Val Loss: 0.1178 | Perfect Match Accuracy: 0.39%
Epoch 0493 | Train Loss: 0.1642 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.37%
Epoch 0494 | Train Loss: 0.1646 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.38%
Epoch 0495 | Train Loss: 0.1669 | Val Loss: 0.1185 | Perfect Match Accuracy: 0.37%
Epoch 0496 | Train Loss: 0.1662 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.38%
Epoch 0497 | Train Loss: 0.1640 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.40%
Epoch 0498 | Train Loss: 0.1638 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.37%
Epoch 0499 | Train Loss: 0.1649 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.39%
Epoch 0500 | Train Loss: 0.1655 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.37%
Epoch 0501 | Train Loss: 0.1636 | Val Loss: 0.1165 | Perfect Match Accuracy: 0.39%
Epoch 0502 | Train Loss: 0.1638 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.38%
Epoch 0503 | Train Loss: 0.1661 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.37%
Epoch 0504 | Train Loss: 0.1666 | Val Loss: 0.1175 | Perfect Match Accuracy: 0.38%
Epoch 0505 | Train Loss: 0.1670 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.39%
Epoch 0506 | Train Loss: 0.1648 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.37%
Epoch 0507 | Train Loss: 0.1644 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.37%
Epoch 0508 | Train Loss: 0.1648 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.39%
Epoch 0509 | Train Loss: 0.1647 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.37%
Epoch 0510 | Train Loss: 0.1647 | Val Loss: 0.1179 | Perfect Match Accuracy: 0.38%
Epoch 0511 | Train Loss: 0.1639 | Val Loss: 0.1194 | Perfect Match Accuracy: 0.36%
Epoch 0512 | Train Loss: 0.1642 | Val Loss: 0.1175 | Perfect Match Accuracy: 0.37%
Epoch 0513 | Train Loss: 0.1635 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.39%
Epoch 0514 | Train Loss: 0.1636 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.38%
Epoch 0515 | Train Loss: 0.1637 | Val Loss: 0.1176 | Perfect Match Accuracy: 0.39%
Epoch 0516 | Train Loss: 0.1639 | Val Loss: 0.1178 | Perfect Match Accuracy: 0.38%
Epoch 0517 | Train Loss: 0.1662 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.39%
Epoch 0518 | Train Loss: 0.1646 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.40%
Epoch 0519 | Train Loss: 0.1648 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.40%
Epoch 0520 | Train Loss: 0.1648 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.38%
Epoch 0521 | Train Loss: 0.1654 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.38%
Epoch 0522 | Train Loss: 0.1651 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.39%
Epoch 0523 | Train Loss: 0.1646 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.39%
Epoch 0524 | Train Loss: 0.1653 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.41%
Epoch 0525 | Train Loss: 0.1658 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.40%
Epoch 0526 | Train Loss: 0.1669 | Val Loss: 0.1192 | Perfect Match Accuracy: 0.37%
Epoch 0527 | Train Loss: 0.1649 | Val Loss: 0.1175 | Perfect Match Accuracy: 0.38%
Epoch 0528 | Train Loss: 0.1628 | Val Loss: 0.1175 | Perfect Match Accuracy: 0.38%
Epoch 0529 | Train Loss: 0.1628 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.37%
Epoch 0530 | Train Loss: 0.1627 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.39%
Epoch 0531 | Train Loss: 0.1630 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.38%
Epoch 0532 | Train Loss: 0.1627 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.37%
Epoch 0533 | Train Loss: 0.1633 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.38%
Epoch 0534 | Train Loss: 0.1614 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.36%
Epoch 0535 | Train Loss: 0.1617 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.37%
Epoch 0536 | Train Loss: 0.1617 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.37%
Epoch 0537 | Train Loss: 0.1622 | Val Loss: 0.1173 | Perfect Match Accuracy: 0.36%
Epoch 0538 | Train Loss: 0.1621 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.37%
Epoch 0539 | Train Loss: 0.1612 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.34%
Epoch 0540 | Train Loss: 0.1615 | Val Loss: 0.1174 | Perfect Match Accuracy: 0.34%
Epoch 0541 | Train Loss: 0.1616 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.35%
Epoch 0542 | Train Loss: 0.1613 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.34%
Epoch 0543 | Train Loss: 0.1611 | Val Loss: 0.1165 | Perfect Match Accuracy: 0.36%
Epoch 0544 | Train Loss: 0.1595 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.34%
Epoch 0545 | Train Loss: 0.1586 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.35%
Epoch 0546 | Train Loss: 0.1581 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.35%
Epoch 0547 | Train Loss: 0.1579 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.35%
Epoch 0548 | Train Loss: 0.1577 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.36%
Epoch 0549 | Train Loss: 0.1580 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.32%
Epoch 0550 | Train Loss: 0.1592 | Val Loss: 0.1165 | Perfect Match Accuracy: 0.31%
Epoch 0551 | Train Loss: 0.1583 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.33%
Epoch 0552 | Train Loss: 0.1585 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.35%
Epoch 0553 | Train Loss: 0.1578 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.35%
Epoch 0554 | Train Loss: 0.1587 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.34%
Epoch 0555 | Train Loss: 0.1585 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.31%
Epoch 0556 | Train Loss: 0.1582 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.32%
Epoch 0557 | Train Loss: 0.1570 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.34%
Epoch 0558 | Train Loss: 0.1567 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.35%
Epoch 0559 | Train Loss: 0.1559 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.30%
Epoch 0560 | Train Loss: 0.1552 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.30%
Epoch 0561 | Train Loss: 0.1553 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.32%
Epoch 0562 | Train Loss: 0.1535 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.31%
Epoch 0563 | Train Loss: 0.1530 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.32%
Epoch 0564 | Train Loss: 0.1516 | Val Loss: 0.1177 | Perfect Match Accuracy: 0.31%
Epoch 0565 | Train Loss: 0.1506 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.30%
Epoch 0566 | Train Loss: 0.1477 | Val Loss: 0.1246 | Perfect Match Accuracy: 0.33%
Epoch 0567 | Train Loss: 0.1584 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.31%
Epoch 0568 | Train Loss: 0.1546 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.32%
Epoch 0569 | Train Loss: 0.1561 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.34%
Epoch 0570 | Train Loss: 0.1572 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.32%
Epoch 0571 | Train Loss: 0.1586 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.31%
Epoch 0572 | Train Loss: 0.1568 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.33%
Epoch 0573 | Train Loss: 0.1549 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.32%
Epoch 0574 | Train Loss: 0.1532 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.33%
Epoch 0575 | Train Loss: 0.1526 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.35%
Epoch 0576 | Train Loss: 0.1529 | Val Loss: 0.1150 | Perfect Match Accuracy: 0.34%
Epoch 0577 | Train Loss: 0.1529 | Val Loss: 0.1150 | Perfect Match Accuracy: 0.35%
Epoch 0578 | Train Loss: 0.1531 | Val Loss: 0.1148 | Perfect Match Accuracy: 0.33%
Epoch 0579 | Train Loss: 0.1531 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.35%
Epoch 0580 | Train Loss: 0.1527 | Val Loss: 0.1151 | Perfect Match Accuracy: 0.32%
Epoch 0581 | Train Loss: 0.1516 | Val Loss: 0.1142 | Perfect Match Accuracy: 0.31%
Epoch 0582 | Train Loss: 0.1523 | Val Loss: 0.1142 | Perfect Match Accuracy: 0.32%
Epoch 0583 | Train Loss: 0.1529 | Val Loss: 0.1146 | Perfect Match Accuracy: 0.34%
Epoch 0584 | Train Loss: 0.1517 | Val Loss: 0.1148 | Perfect Match Accuracy: 0.33%
Epoch 0585 | Train Loss: 0.1516 | Val Loss: 0.1143 | Perfect Match Accuracy: 0.34%
Epoch 0586 | Train Loss: 0.1518 | Val Loss: 0.1139 | Perfect Match Accuracy: 0.33%
Epoch 0587 | Train Loss: 0.1520 | Val Loss: 0.1148 | Perfect Match Accuracy: 0.32%
Epoch 0588 | Train Loss: 0.1509 | Val Loss: 0.1146 | Perfect Match Accuracy: 0.33%
Epoch 0589 | Train Loss: 0.1506 | Val Loss: 0.1139 | Perfect Match Accuracy: 0.31%
Epoch 0590 | Train Loss: 0.1502 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.30%
Epoch 0591 | Train Loss: 0.1505 | Val Loss: 0.1144 | Perfect Match Accuracy: 0.34%
Epoch 0592 | Train Loss: 0.1510 | Val Loss: 0.1147 | Perfect Match Accuracy: 0.34%
Epoch 0593 | Train Loss: 0.1516 | Val Loss: 0.1147 | Perfect Match Accuracy: 0.34%
Epoch 0594 | Train Loss: 0.1519 | Val Loss: 0.1144 | Perfect Match Accuracy: 0.35%
Epoch 0595 | Train Loss: 0.1534 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.34%
Epoch 0596 | Train Loss: 0.1526 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.34%
Epoch 0597 | Train Loss: 0.1536 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.37%
Epoch 0598 | Train Loss: 0.1533 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.37%
Epoch 0599 | Train Loss: 0.1528 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.34%
Epoch 0600 | Train Loss: 0.1540 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.35%
Epoch 0601 | Train Loss: 0.1548 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.37%
Epoch 0602 | Train Loss: 0.1531 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.35%
Epoch 0603 | Train Loss: 0.1530 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.35%
Epoch 0604 | Train Loss: 0.1526 | Val Loss: 0.1165 | Perfect Match Accuracy: 0.36%
Epoch 0605 | Train Loss: 0.1524 | Val Loss: 0.1151 | Perfect Match Accuracy: 0.36%
Epoch 0606 | Train Loss: 0.1525 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.37%
Epoch 0607 | Train Loss: 0.1526 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.35%
Epoch 0608 | Train Loss: 0.1526 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.37%
Epoch 0609 | Train Loss: 0.1514 | Val Loss: 0.1150 | Perfect Match Accuracy: 0.36%
Epoch 0610 | Train Loss: 0.1510 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.35%
Epoch 0611 | Train Loss: 0.1509 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.34%
Epoch 0612 | Train Loss: 0.1512 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.37%
Epoch 0613 | Train Loss: 0.1517 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.35%
Epoch 0614 | Train Loss: 0.1542 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.35%
Epoch 0615 | Train Loss: 0.1524 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.37%
Epoch 0616 | Train Loss: 0.1528 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.37%
Epoch 0617 | Train Loss: 0.1531 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.34%
Epoch 0618 | Train Loss: 0.1537 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.35%
Epoch 0619 | Train Loss: 0.1540 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.38%
Epoch 0620 | Train Loss: 0.1531 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.37%
Epoch 0621 | Train Loss: 0.1527 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.34%
Epoch 0622 | Train Loss: 0.1541 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.33%
Epoch 0623 | Train Loss: 0.1552 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.37%
Epoch 0624 | Train Loss: 0.1553 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.38%
Epoch 0625 | Train Loss: 0.1565 | Val Loss: 0.1147 | Perfect Match Accuracy: 0.37%
Epoch 0626 | Train Loss: 0.1567 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.34%
Epoch 0627 | Train Loss: 0.1584 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.35%
Epoch 0628 | Train Loss: 0.1583 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.36%
Epoch 0629 | Train Loss: 0.1583 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.35%
Epoch 0630 | Train Loss: 0.1584 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.33%
Epoch 0631 | Train Loss: 0.1584 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.36%
Epoch 0632 | Train Loss: 0.1604 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.38%
Epoch 0633 | Train Loss: 0.1595 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.38%
Epoch 0634 | Train Loss: 0.1602 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.36%
Epoch 0635 | Train Loss: 0.1592 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.38%
Epoch 0636 | Train Loss: 0.1590 | Val Loss: 0.1151 | Perfect Match Accuracy: 0.36%
Epoch 0637 | Train Loss: 0.1614 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.38%
Epoch 0638 | Train Loss: 0.1620 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.36%
Epoch 0639 | Train Loss: 0.1608 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.36%
Epoch 0640 | Train Loss: 0.1616 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.38%
Epoch 0641 | Train Loss: 0.1622 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.38%
Epoch 0642 | Train Loss: 0.1627 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.37%
Epoch 0643 | Train Loss: 0.1641 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.35%
Epoch 0644 | Train Loss: 0.1650 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.38%
Epoch 0645 | Train Loss: 0.1669 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.36%
Epoch 0646 | Train Loss: 0.1669 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.35%
Epoch 0647 | Train Loss: 0.1655 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.37%
Epoch 0648 | Train Loss: 0.1658 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.34%
Epoch 0649 | Train Loss: 0.1656 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.37%
Epoch 0650 | Train Loss: 0.1671 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.39%
Epoch 0651 | Train Loss: 0.1658 | Val Loss: 0.1151 | Perfect Match Accuracy: 0.38%
Epoch 0652 | Train Loss: 0.1649 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.37%
Epoch 0653 | Train Loss: 0.1649 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.39%
Epoch 0654 | Train Loss: 0.1648 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.38%
Epoch 0655 | Train Loss: 0.1653 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.38%
Epoch 0656 | Train Loss: 0.1666 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.41%
Epoch 0657 | Train Loss: 0.1681 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.40%
Epoch 0658 | Train Loss: 0.1685 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.41%
Epoch 0659 | Train Loss: 0.1686 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.41%
Epoch 0660 | Train Loss: 0.1695 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.39%
Epoch 0661 | Train Loss: 0.1702 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.40%
Epoch 0662 | Train Loss: 0.1700 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.40%
Epoch 0663 | Train Loss: 0.1689 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.37%
Epoch 0664 | Train Loss: 0.1687 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.39%
Epoch 0665 | Train Loss: 0.1688 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.42%
Epoch 0666 | Train Loss: 0.1692 | Val Loss: 0.1171 | Perfect Match Accuracy: 0.39%
Epoch 0667 | Train Loss: 0.1697 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.39%
Epoch 0668 | Train Loss: 0.1702 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.39%
Epoch 0669 | Train Loss: 0.1708 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.41%
Epoch 0670 | Train Loss: 0.1717 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.38%
Epoch 0671 | Train Loss: 0.1728 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.41%
Epoch 0672 | Train Loss: 0.1732 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.39%
Epoch 0673 | Train Loss: 0.1730 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.40%
Epoch 0674 | Train Loss: 0.1729 | Val Loss: 0.1174 | Perfect Match Accuracy: 0.39%
Epoch 0675 | Train Loss: 0.1743 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.43%
Epoch 0676 | Train Loss: 0.1744 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.39%
Epoch 0677 | Train Loss: 0.1748 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.38%
Epoch 0678 | Train Loss: 0.1743 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.40%
Epoch 0679 | Train Loss: 0.1748 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.38%
Epoch 0680 | Train Loss: 0.1746 | Val Loss: 0.1189 | Perfect Match Accuracy: 0.38%
Epoch 0681 | Train Loss: 0.1753 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.38%
Epoch 0682 | Train Loss: 0.1746 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.39%
Epoch 0683 | Train Loss: 0.1748 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.39%
Epoch 0684 | Train Loss: 0.1739 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.39%
Epoch 0685 | Train Loss: 0.1739 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.37%
Epoch 0686 | Train Loss: 0.1745 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.40%
Epoch 0687 | Train Loss: 0.1744 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.37%
Epoch 0688 | Train Loss: 0.1749 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.39%
Epoch 0689 | Train Loss: 0.1753 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.39%
Epoch 0690 | Train Loss: 0.1756 | Val Loss: 0.1165 | Perfect Match Accuracy: 0.39%
Epoch 0691 | Train Loss: 0.1757 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.39%
Epoch 0692 | Train Loss: 0.1759 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.39%
Epoch 0693 | Train Loss: 0.1760 | Val Loss: 0.1177 | Perfect Match Accuracy: 0.38%
Epoch 0694 | Train Loss: 0.1758 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.36%
Epoch 0695 | Train Loss: 0.1760 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.38%
Epoch 0696 | Train Loss: 0.1762 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.38%
Epoch 0697 | Train Loss: 0.1767 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.37%
Epoch 0698 | Train Loss: 0.1766 | Val Loss: 0.1175 | Perfect Match Accuracy: 0.39%
Epoch 0699 | Train Loss: 0.1768 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.39%
Epoch 0700 | Train Loss: 0.1769 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.39%
Epoch 0701 | Train Loss: 0.1764 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.40%
Epoch 0702 | Train Loss: 0.1761 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.40%
Epoch 0703 | Train Loss: 0.1760 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.38%
Epoch 0704 | Train Loss: 0.1762 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.38%
Epoch 0705 | Train Loss: 0.1761 | Val Loss: 0.1181 | Perfect Match Accuracy: 0.37%
Epoch 0706 | Train Loss: 0.1765 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.39%
Epoch 0707 | Train Loss: 0.1756 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.38%
Epoch 0708 | Train Loss: 0.1755 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.38%
Epoch 0709 | Train Loss: 0.1748 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.36%
Epoch 0710 | Train Loss: 0.1750 | Val Loss: 0.1174 | Perfect Match Accuracy: 0.38%
Epoch 0711 | Train Loss: 0.1745 | Val Loss: 0.1173 | Perfect Match Accuracy: 0.37%
Epoch 0712 | Train Loss: 0.1723 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.39%
Epoch 0713 | Train Loss: 0.1727 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.37%
Epoch 0714 | Train Loss: 0.1728 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.38%
Epoch 0715 | Train Loss: 0.1718 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.37%
Epoch 0716 | Train Loss: 0.1712 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.39%
Epoch 0717 | Train Loss: 0.1713 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.38%
Epoch 0718 | Train Loss: 0.1712 | Val Loss: 0.1170 | Perfect Match Accuracy: 0.36%
Epoch 0719 | Train Loss: 0.1715 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.37%
Epoch 0720 | Train Loss: 0.1719 | Val Loss: 0.1177 | Perfect Match Accuracy: 0.38%
Epoch 0721 | Train Loss: 0.1719 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.39%
Epoch 0722 | Train Loss: 0.1720 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.37%
Epoch 0723 | Train Loss: 0.1719 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.38%
Epoch 0724 | Train Loss: 0.1721 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.38%
Epoch 0725 | Train Loss: 0.1717 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.36%
Epoch 0726 | Train Loss: 0.1718 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.36%
Epoch 0727 | Train Loss: 0.1716 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.37%
Epoch 0728 | Train Loss: 0.1718 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.38%
Epoch 0729 | Train Loss: 0.1717 | Val Loss: 0.1167 | Perfect Match Accuracy: 0.35%
Epoch 0730 | Train Loss: 0.1703 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.36%
Epoch 0731 | Train Loss: 0.1700 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.41%
Epoch 0732 | Train Loss: 0.1702 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.39%
Epoch 0733 | Train Loss: 0.1706 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.37%
Epoch 0734 | Train Loss: 0.1707 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.40%
Epoch 0735 | Train Loss: 0.1710 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.36%
Epoch 0736 | Train Loss: 0.1702 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.40%
Epoch 0737 | Train Loss: 0.1699 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.41%
Epoch 0738 | Train Loss: 0.1703 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.37%
Epoch 0739 | Train Loss: 0.1707 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.40%
Epoch 0740 | Train Loss: 0.1712 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.38%
Epoch 0741 | Train Loss: 0.1707 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.40%
Epoch 0742 | Train Loss: 0.1705 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.40%
Epoch 0743 | Train Loss: 0.1704 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.38%
Epoch 0744 | Train Loss: 0.1701 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.37%
Epoch 0745 | Train Loss: 0.1700 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.36%
Epoch 0746 | Train Loss: 0.1684 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.37%
Epoch 0747 | Train Loss: 0.1674 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.36%
Epoch 0748 | Train Loss: 0.1667 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.36%
Epoch 0749 | Train Loss: 0.1667 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.37%
Epoch 0750 | Train Loss: 0.1666 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.38%
Epoch 0751 | Train Loss: 0.1664 | Val Loss: 0.1213 | Perfect Match Accuracy: 0.35%
Epoch 0752 | Train Loss: 0.1654 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.33%
Epoch 0753 | Train Loss: 0.1644 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.35%
Epoch 0754 | Train Loss: 0.1646 | Val Loss: 0.1168 | Perfect Match Accuracy: 0.37%
Epoch 0755 | Train Loss: 0.1646 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.35%
Epoch 0756 | Train Loss: 0.1638 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.35%
Epoch 0757 | Train Loss: 0.1634 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.34%
Epoch 0758 | Train Loss: 0.1619 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.35%
Epoch 0759 | Train Loss: 0.1614 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.37%
Epoch 0760 | Train Loss: 0.1617 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.35%
Epoch 0761 | Train Loss: 0.1605 | Val Loss: 0.1165 | Perfect Match Accuracy: 0.30%
Epoch 0762 | Train Loss: 0.1600 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.34%
Epoch 0763 | Train Loss: 0.1605 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.36%
Epoch 0764 | Train Loss: 0.1601 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.34%
Epoch 0765 | Train Loss: 0.1605 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.34%
Epoch 0766 | Train Loss: 0.1608 | Val Loss: 0.1152 | Perfect Match Accuracy: 0.36%
Epoch 0767 | Train Loss: 0.1630 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.36%
Epoch 0768 | Train Loss: 0.1619 | Val Loss: 0.1148 | Perfect Match Accuracy: 0.38%
Epoch 0769 | Train Loss: 0.1609 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.39%
Epoch 0770 | Train Loss: 0.1610 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.35%
Epoch 0771 | Train Loss: 0.1618 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.34%
Epoch 0772 | Train Loss: 0.1600 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.34%
Epoch 0773 | Train Loss: 0.1590 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.36%
Epoch 0774 | Train Loss: 0.1584 | Val Loss: 0.1149 | Perfect Match Accuracy: 0.33%
Epoch 0775 | Train Loss: 0.1588 | Val Loss: 0.1178 | Perfect Match Accuracy: 0.34%
Epoch 0776 | Train Loss: 0.1571 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.35%
Epoch 0777 | Train Loss: 0.1582 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.37%
Epoch 0778 | Train Loss: 0.1585 | Val Loss: 0.1144 | Perfect Match Accuracy: 0.35%
Epoch 0779 | Train Loss: 0.1580 | Val Loss: 0.1153 | Perfect Match Accuracy: 0.33%
Epoch 0780 | Train Loss: 0.1580 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.35%
Epoch 0781 | Train Loss: 0.1582 | Val Loss: 0.1166 | Perfect Match Accuracy: 0.37%
Epoch 0782 | Train Loss: 0.1585 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.38%
Epoch 0783 | Train Loss: 0.1587 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.32%
Epoch 0784 | Train Loss: 0.1587 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.33%
Epoch 0785 | Train Loss: 0.1583 | Val Loss: 0.1179 | Perfect Match Accuracy: 0.31%
Epoch 0786 | Train Loss: 0.1573 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.32%
Epoch 0787 | Train Loss: 0.1562 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.37%
Epoch 0788 | Train Loss: 0.1566 | Val Loss: 0.1164 | Perfect Match Accuracy: 0.35%
Epoch 0789 | Train Loss: 0.1576 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.35%
Epoch 0790 | Train Loss: 0.1573 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.35%
Epoch 0791 | Train Loss: 0.1570 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.34%
Epoch 0792 | Train Loss: 0.1573 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.32%
Epoch 0793 | Train Loss: 0.1574 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.34%
Epoch 0794 | Train Loss: 0.1563 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.31%
Epoch 0795 | Train Loss: 0.1557 | Val Loss: 0.1158 | Perfect Match Accuracy: 0.35%
Epoch 0796 | Train Loss: 0.1553 | Val Loss: 0.1150 | Perfect Match Accuracy: 0.35%
Epoch 0797 | Train Loss: 0.1544 | Val Loss: 0.1156 | Perfect Match Accuracy: 0.36%
Epoch 0798 | Train Loss: 0.1559 | Val Loss: 0.1175 | Perfect Match Accuracy: 0.29%
Epoch 0799 | Train Loss: 0.1550 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.36%
Epoch 0800 | Train Loss: 0.1524 | Val Loss: 0.1160 | Perfect Match Accuracy: 0.34%
Epoch 0801 | Train Loss: 0.1518 | Val Loss: 0.1150 | Perfect Match Accuracy: 0.33%
Epoch 0802 | Train Loss: 0.1516 | Val Loss: 0.1161 | Perfect Match Accuracy: 0.33%
Epoch 0803 | Train Loss: 0.1493 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.35%
Epoch 0804 | Train Loss: 0.1493 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.33%
Epoch 0805 | Train Loss: 0.1507 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.36%
Epoch 0806 | Train Loss: 0.1520 | Val Loss: 0.1169 | Perfect Match Accuracy: 0.35%
Epoch 0807 | Train Loss: 0.1534 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.37%
Epoch 0808 | Train Loss: 0.1545 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.34%
Epoch 0809 | Train Loss: 0.1544 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.33%
Epoch 0810 | Train Loss: 0.1544 | Val Loss: 0.1162 | Perfect Match Accuracy: 0.33%
Epoch 0811 | Train Loss: 0.1543 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.31%
Epoch 0812 | Train Loss: 0.1556 | Val Loss: 0.1157 | Perfect Match Accuracy: 0.28%
Epoch 0813 | Train Loss: 0.1555 | Val Loss: 0.1159 | Perfect Match Accuracy: 0.32%
Epoch 0814 | Train Loss: 0.1551 | Val Loss: 0.1154 | Perfect Match Accuracy: 0.31%
Epoch 0815 | Train Loss: 0.1559 | Val Loss: 0.1172 | Perfect Match Accuracy: 0.29%
Epoch 0816 | Train Loss: 0.1571 | Val Loss: 0.1155 | Perfect Match Accuracy: 0.32%
Epoch 0817 | Train Loss: 0.1616 | Val Loss: 0.1224 | Perfect Match Accuracy: 0.26%
Epoch 0818 | Train Loss: 0.1652 | Val Loss: 0.1178 | Perfect Match Accuracy: 0.29%
Epoch 0819 | Train Loss: 0.1531 | Val Loss: 0.1201 | Perfect Match Accuracy: 0.30%
Epoch 0820 | Train Loss: 0.1246 | Val Loss: 0.1163 | Perfect Match Accuracy: 0.34%
Epoch 0821 | Train Loss: 0.1533 | Val Loss: 0.1223 | Perfect Match Accuracy: 0.27%
Epoch 0822 | Train Loss: 0.2478 | Val Loss: 0.1323 | Perfect Match Accuracy: 0.27%
Epoch 0823 | Train Loss: 0.2540 | Val Loss: 0.1284 | Perfect Match Accuracy: 0.25%
Epoch 0824 | Train Loss: 0.2630 | Val Loss: 0.1284 | Perfect Match Accuracy: 0.29%
Epoch 0825 | Train Loss: 0.2541 | Val Loss: 0.1300 | Perfect Match Accuracy: 0.28%
Epoch 0826 | Train Loss: 0.2589 | Val Loss: 0.1245 | Perfect Match Accuracy: 0.27%
Epoch 0827 | Train Loss: 0.2885 | Val Loss: 0.1234 | Perfect Match Accuracy: 0.30%
Epoch 0828 | Train Loss: 0.3072 | Val Loss: 0.1234 | Perfect Match Accuracy: 0.32%
Epoch 0829 | Train Loss: 0.3205 | Val Loss: 0.1259 | Perfect Match Accuracy: 0.31%
Epoch 0830 | Train Loss: 0.3287 | Val Loss: 0.1218 | Perfect Match Accuracy: 0.29%
Epoch 0831 | Train Loss: 0.3294 | Val Loss: 0.1270 | Perfect Match Accuracy: 0.27%
Epoch 0832 | Train Loss: 0.3141 | Val Loss: 0.1220 | Perfect Match Accuracy: 0.29%
Epoch 0833 | Train Loss: 0.2963 | Val Loss: 0.1277 | Perfect Match Accuracy: 0.26%
Epoch 0834 | Train Loss: 0.2990 | Val Loss: 0.1287 | Perfect Match Accuracy: 0.27%
Epoch 0835 | Train Loss: 0.3158 | Val Loss: 0.1217 | Perfect Match Accuracy: 0.30%
Epoch 0836 | Train Loss: 0.2612 | Val Loss: 0.1240 | Perfect Match Accuracy: 0.27%
Epoch 0837 | Train Loss: 0.2759 | Val Loss: 0.1266 | Perfect Match Accuracy: 0.31%
Epoch 0838 | Train Loss: 0.2733 | Val Loss: 0.1244 | Perfect Match Accuracy: 0.27%
Epoch 0839 | Train Loss: 0.2721 | Val Loss: 0.1229 | Perfect Match Accuracy: 0.30%
Epoch 0840 | Train Loss: 0.2509 | Val Loss: 0.1212 | Perfect Match Accuracy: 0.29%
Epoch 0841 | Train Loss: 0.2578 | Val Loss: 0.1233 | Perfect Match Accuracy: 0.31%
Epoch 0842 | Train Loss: 0.2625 | Val Loss: 0.1204 | Perfect Match Accuracy: 0.32%
Epoch 0843 | Train Loss: 0.2644 | Val Loss: 0.1219 | Perfect Match Accuracy: 0.30%
Epoch 0844 | Train Loss: 0.2656 | Val Loss: 0.1227 | Perfect Match Accuracy: 0.31%
Epoch 0845 | Train Loss: 0.2675 | Val Loss: 0.1221 | Perfect Match Accuracy: 0.29%
Epoch 0846 | Train Loss: 0.2869 | Val Loss: 0.1249 | Perfect Match Accuracy: 0.31%
Epoch 0847 | Train Loss: 0.2966 | Val Loss: 0.1207 | Perfect Match Accuracy: 0.31%
Epoch 0848 | Train Loss: 0.2920 | Val Loss: 0.1252 | Perfect Match Accuracy: 0.30%
Epoch 0849 | Train Loss: 0.3021 | Val Loss: 0.1245 | Perfect Match Accuracy: 0.31%
Epoch 0850 | Train Loss: 0.3020 | Val Loss: 0.1226 | Perfect Match Accuracy: 0.32%
Epoch 0851 | Train Loss: 0.3091 | Val Loss: 0.1254 | Perfect Match Accuracy: 0.33%
Epoch 0852 | Train Loss: 0.3122 | Val Loss: 0.1251 | Perfect Match Accuracy: 0.34%
Epoch 0853 | Train Loss: 0.3158 | Val Loss: 0.1241 | Perfect Match Accuracy: 0.35%
Epoch 0854 | Train Loss: 0.3179 | Val Loss: 0.1254 | Perfect Match Accuracy: 0.33%
Epoch 0855 | Train Loss: 0.3240 | Val Loss: 0.1242 | Perfect Match Accuracy: 0.30%
Epoch 0856 | Train Loss: 0.3245 | Val Loss: 0.1244 | Perfect Match Accuracy: 0.32%
Epoch 0857 | Train Loss: 0.3290 | Val Loss: 0.1246 | Perfect Match Accuracy: 0.32%
Epoch 0858 | Train Loss: 0.3318 | Val Loss: 0.1277 | Perfect Match Accuracy: 0.31%
Epoch 0859 | Train Loss: 0.3349 | Val Loss: 0.1218 | Perfect Match Accuracy: 0.29%
Epoch 0860 | Train Loss: 0.3366 | Val Loss: 0.1247 | Perfect Match Accuracy: 0.29%
Epoch 0861 | Train Loss: 0.3392 | Val Loss: 0.1229 | Perfect Match Accuracy: 0.29%
Epoch 0862 | Train Loss: 0.3386 | Val Loss: 0.1227 | Perfect Match Accuracy: 0.29%
Epoch 0863 | Train Loss: 0.3394 | Val Loss: 0.1247 | Perfect Match Accuracy: 0.31%
Epoch 0864 | Train Loss: 0.3383 | Val Loss: 0.1238 | Perfect Match Accuracy: 0.31%
Epoch 0865 | Train Loss: 0.3410 | Val Loss: 0.1242 | Perfect Match Accuracy: 0.30%
Epoch 0866 | Train Loss: 0.3405 | Val Loss: 0.1247 | Perfect Match Accuracy: 0.31%
Epoch 0867 | Train Loss: 0.3389 | Val Loss: 0.1253 | Perfect Match Accuracy: 0.33%
Epoch 0868 | Train Loss: 0.3407 | Val Loss: 0.1239 | Perfect Match Accuracy: 0.32%
Epoch 0869 | Train Loss: 0.3409 | Val Loss: 0.1244 | Perfect Match Accuracy: 0.31%
Epoch 0870 | Train Loss: 0.3411 | Val Loss: 0.1233 | Perfect Match Accuracy: 0.31%
Epoch 0871 | Train Loss: 0.3419 | Val Loss: 0.1233 | Perfect Match Accuracy: 0.32%
Epoch 0872 | Train Loss: 0.3411 | Val Loss: 0.1288 | Perfect Match Accuracy: 0.32%
Epoch 0873 | Train Loss: 0.3417 | Val Loss: 0.1233 | Perfect Match Accuracy: 0.35%
Epoch 0874 | Train Loss: 0.3423 | Val Loss: 0.1284 | Perfect Match Accuracy: 0.34%
Epoch 0875 | Train Loss: 0.3421 | Val Loss: 0.1252 | Perfect Match Accuracy: 0.33%
Epoch 0876 | Train Loss: 0.3301 | Val Loss: 0.1285 | Perfect Match Accuracy: 0.34%
Epoch 0877 | Train Loss: 0.3368 | Val Loss: 0.1377 | Perfect Match Accuracy: 0.32%
Epoch 0878 | Train Loss: 0.3248 | Val Loss: 0.1237 | Perfect Match Accuracy: 0.34%
Epoch 0879 | Train Loss: 0.3257 | Val Loss: 0.1252 | Perfect Match Accuracy: 0.31%
Epoch 0880 | Train Loss: 0.3293 | Val Loss: 0.1277 | Perfect Match Accuracy: 0.31%
Epoch 0881 | Train Loss: 0.3307 | Val Loss: 0.1255 | Perfect Match Accuracy: 0.30%
Epoch 0882 | Train Loss: 0.3303 | Val Loss: 0.1247 | Perfect Match Accuracy: 0.31%
Epoch 0883 | Train Loss: 0.3369 | Val Loss: 0.1295 | Perfect Match Accuracy: 0.30%
Epoch 0884 | Train Loss: 0.3516 | Val Loss: 0.1300 | Perfect Match Accuracy: 0.30%
Epoch 0885 | Train Loss: 0.3539 | Val Loss: 0.1280 | Perfect Match Accuracy: 0.30%
Epoch 0886 | Train Loss: 0.3543 | Val Loss: 0.1328 | Perfect Match Accuracy: 0.30%
Epoch 0887 | Train Loss: 0.3512 | Val Loss: 0.1261 | Perfect Match Accuracy: 0.31%
Epoch 0888 | Train Loss: 0.3526 | Val Loss: 0.1324 | Perfect Match Accuracy: 0.31%
Epoch 0889 | Train Loss: 0.3550 | Val Loss: 0.1307 | Perfect Match Accuracy: 0.31%
Epoch 0890 | Train Loss: 0.3483 | Val Loss: 0.1277 | Perfect Match Accuracy: 0.30%
Epoch 0891 | Train Loss: 0.3471 | Val Loss: 0.1308 | Perfect Match Accuracy: 0.31%
Epoch 0892 | Train Loss: 0.3468 | Val Loss: 0.1282 | Perfect Match Accuracy: 0.30%
Epoch 0893 | Train Loss: 0.3499 | Val Loss: 0.1276 | Perfect Match Accuracy: 0.31%
Epoch 0894 | Train Loss: 0.3480 | Val Loss: 0.1333 | Perfect Match Accuracy: 0.32%
Epoch 0895 | Train Loss: 0.3491 | Val Loss: 0.1274 | Perfect Match Accuracy: 0.32%
Epoch 0896 | Train Loss: 0.3490 | Val Loss: 0.1293 | Perfect Match Accuracy: 0.32%
Epoch 0897 | Train Loss: 0.3490 | Val Loss: 0.1278 | Perfect Match Accuracy: 0.32%
Epoch 0898 | Train Loss: 0.3495 | Val Loss: 0.1257 | Perfect Match Accuracy: 0.31%
Epoch 0899 | Train Loss: 0.3512 | Val Loss: 0.1298 | Perfect Match Accuracy: 0.32%
Epoch 0900 | Train Loss: 0.3494 | Val Loss: 0.1314 | Perfect Match Accuracy: 0.31%
Epoch 0901 | Train Loss: 0.3507 | Val Loss: 0.1298 | Perfect Match Accuracy: 0.32%
Epoch 0902 | Train Loss: 0.3504 | Val Loss: 0.1294 | Perfect Match Accuracy: 0.31%
Epoch 0903 | Train Loss: 0.3511 | Val Loss: 0.1252 | Perfect Match Accuracy: 0.32%
Epoch 0904 | Train Loss: 0.3526 | Val Loss: 0.1327 | Perfect Match Accuracy: 0.30%
Epoch 0905 | Train Loss: 0.3504 | Val Loss: 0.1279 | Perfect Match Accuracy: 0.31%
Epoch 0906 | Train Loss: 0.3499 | Val Loss: 0.1271 | Perfect Match Accuracy: 0.32%
Epoch 0907 | Train Loss: 0.3496 | Val Loss: 0.1248 | Perfect Match Accuracy: 0.33%
Epoch 0908 | Train Loss: 0.3502 | Val Loss: 0.1313 | Perfect Match Accuracy: 0.32%
Epoch 0909 | Train Loss: 0.3502 | Val Loss: 0.1255 | Perfect Match Accuracy: 0.31%
Epoch 0910 | Train Loss: 0.3491 | Val Loss: 0.1247 | Perfect Match Accuracy: 0.32%
Epoch 0911 | Train Loss: 0.3497 | Val Loss: 0.1264 | Perfect Match Accuracy: 0.32%
Epoch 0912 | Train Loss: 0.3481 | Val Loss: 0.1243 | Perfect Match Accuracy: 0.33%
Epoch 0913 | Train Loss: 0.3473 | Val Loss: 0.1284 | Perfect Match Accuracy: 0.32%
Epoch 0914 | Train Loss: 0.3471 | Val Loss: 0.1277 | Perfect Match Accuracy: 0.34%
Epoch 0915 | Train Loss: 0.3485 | Val Loss: 0.1260 | Perfect Match Accuracy: 0.34%
Epoch 0916 | Train Loss: 0.3444 | Val Loss: 0.1352 | Perfect Match Accuracy: 0.34%
Epoch 0917 | Train Loss: 0.3477 | Val Loss: 0.1265 | Perfect Match Accuracy: 0.34%
Epoch 0918 | Train Loss: 0.3603 | Val Loss: 0.1308 | Perfect Match Accuracy: 0.30%
Epoch 0919 | Train Loss: 0.3502 | Val Loss: 0.1251 | Perfect Match Accuracy: 0.31%
Epoch 0920 | Train Loss: 0.3185 | Val Loss: 0.1253 | Perfect Match Accuracy: 0.32%
Epoch 0921 | Train Loss: 0.3135 | Val Loss: 0.1231 | Perfect Match Accuracy: 0.31%
Epoch 0922 | Train Loss: 0.3109 | Val Loss: 0.1266 | Perfect Match Accuracy: 0.32%
Epoch 0923 | Train Loss: 0.3100 | Val Loss: 0.1228 | Perfect Match Accuracy: 0.33%
Epoch 0924 | Train Loss: 0.3097 | Val Loss: 0.1242 | Perfect Match Accuracy: 0.34%
Epoch 0925 | Train Loss: 0.3094 | Val Loss: 0.1229 | Perfect Match Accuracy: 0.34%
Epoch 0926 | Train Loss: 0.3090 | Val Loss: 0.1227 | Perfect Match Accuracy: 0.33%
Epoch 0927 | Train Loss: 0.3070 | Val Loss: 0.1236 | Perfect Match Accuracy: 0.32%
Epoch 0928 | Train Loss: 0.3072 | Val Loss: 0.1222 | Perfect Match Accuracy: 0.34%
Epoch 0929 | Train Loss: 0.3056 | Val Loss: 0.1256 | Perfect Match Accuracy: 0.32%
Epoch 0930 | Train Loss: 0.3081 | Val Loss: 0.1216 | Perfect Match Accuracy: 0.30%
Epoch 0931 | Train Loss: 0.3068 | Val Loss: 0.1233 | Perfect Match Accuracy: 0.32%
Epoch 0932 | Train Loss: 0.3291 | Val Loss: 0.1274 | Perfect Match Accuracy: 0.32%
Epoch 0933 | Train Loss: 0.3042 | Val Loss: 0.1214 | Perfect Match Accuracy: 0.31%
Epoch 0934 | Train Loss: 0.2954 | Val Loss: 0.1276 | Perfect Match Accuracy: 0.34%
Epoch 0935 | Train Loss: 0.3021 | Val Loss: 0.1227 | Perfect Match Accuracy: 0.31%
Epoch 0936 | Train Loss: 0.3024 | Val Loss: 0.1226 | Perfect Match Accuracy: 0.32%
Epoch 0937 | Train Loss: 0.3034 | Val Loss: 0.1225 | Perfect Match Accuracy: 0.32%
"""

def parse_and_plot(text):
    epochs = []
    train_losses = []
    val_losses = []
    accuracies = []

    # Regex pattern to capture numbers dynamically
    pattern = re.compile(
        r"Epoch\s+(\d+)\s*\|\s*Train Loss:\s*([\d.]+)\s*\|\s*Val Loss:\s*([\d.]+)\s*\|\s*Perfect Match Accuracy:\s*([\d.]+)%"
    )

    # Process line by line iteratively
    for line in text.strip().split("\n"):
        match = pattern.search(line)
        if match:
            epoch = int(match.group(1))
            train_loss = float(match.group(2))
            val_loss = float(match.group(3))
            accuracy = float(match.group(4))

            epochs.append(epoch)
            train_losses.append(train_loss)
            val_losses.append(val_loss)
            accuracies.append(accuracy)

    # Building the Dual-Y-Axis Chart
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Left Y-Axis: Losses
    color_train = '#1f77b4'
    color_val = '#ff7f0e'
    ax1.set_xlabel('Epoch', fontweight='bold')
    ax1.set_ylabel('Loss', color='black', fontweight='bold')
    line1 = ax1.plot(epochs, train_losses, color=color_train, marker='o', label='Train Loss', linewidth=2)
    line2 = ax1.plot(epochs, val_losses, color=color_val, marker='s', label='Val Loss', linewidth=2)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Right Y-Axis: Accuracy (Since percentages are on a completely different scale than loss numbers)
    ax2 = ax1.twinx()  
    color_acc = '#2ca02c'
    ax2.set_ylabel('Perfect Match Accuracy (%)', color=color_acc, fontweight='bold')
    line3 = ax2.plot(epochs, accuracies, color=color_acc, marker='^', linestyle='--', label='Accuracy (%)', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color_acc)

    # Combine legends from both axes
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')

    plt.title('Modulo Net VQ Training Performance History', fontsize=14, fontweight='bold', pad=15)
    fig.tight_layout()
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    parse_and_plot(log_data)
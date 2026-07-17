import re
import matplotlib.pyplot as plt

# The text data containing the training history with soft accuracy formatting
log_data = """
Epoch 0001 | Train Loss: 0.1242 (Soft Acc: 95.41%) | Val Loss: 0.1169 (Soft Acc: 95.54%) | Perfect Match: 0.00% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0002 | Train Loss: 0.1150 (Soft Acc: 95.57%) | Val Loss: 0.0988 (Soft Acc: 96.43%) | Perfect Match: 0.45% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0003 | Train Loss: 0.0994 (Soft Acc: 96.35%) | Val Loss: 0.0743 (Soft Acc: 97.52%) | Perfect Match: 2.50% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0004 | Train Loss: 0.0866 (Soft Acc: 96.98%) | Val Loss: 0.0698 (Soft Acc: 97.69%) | Perfect Match: 2.79% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0005 | Train Loss: 0.0802 (Soft Acc: 97.26%) | Val Loss: 0.0673 (Soft Acc: 97.80%) | Perfect Match: 2.97% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0006 | Train Loss: 0.0766 (Soft Acc: 97.42%) | Val Loss: 0.0655 (Soft Acc: 97.87%) | Perfect Match: 3.16% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0007 | Train Loss: 0.0741 (Soft Acc: 97.53%) | Val Loss: 0.0643 (Soft Acc: 97.92%) | Perfect Match: 3.31% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0008 | Train Loss: 0.0723 (Soft Acc: 97.60%) | Val Loss: 0.0633 (Soft Acc: 97.95%) | Perfect Match: 3.47% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0009 | Train Loss: 0.0708 (Soft Acc: 97.66%) | Val Loss: 0.0625 (Soft Acc: 97.99%) | Perfect Match: 3.63% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0010 | Train Loss: 0.0696 (Soft Acc: 97.71%) | Val Loss: 0.0619 (Soft Acc: 98.00%) | Perfect Match: 3.69% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0011 | Train Loss: 0.0686 (Soft Acc: 97.75%) | Val Loss: 0.0615 (Soft Acc: 98.02%) | Perfect Match: 3.77% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0012 | Train Loss: 0.0679 (Soft Acc: 97.78%) | Val Loss: 0.0612 (Soft Acc: 98.03%) | Perfect Match: 3.81% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0013 | Train Loss: 0.0672 (Soft Acc: 97.81%) | Val Loss: 0.0610 (Soft Acc: 98.04%) | Perfect Match: 3.87% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0014 | Train Loss: 0.0667 (Soft Acc: 97.83%) | Val Loss: 0.0608 (Soft Acc: 98.04%) | Perfect Match: 3.89% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0015 | Train Loss: 0.0662 (Soft Acc: 97.85%) | Val Loss: 0.0606 (Soft Acc: 98.05%) | Perfect Match: 3.92% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0016 | Train Loss: 0.0657 (Soft Acc: 97.86%) | Val Loss: 0.0604 (Soft Acc: 98.06%) | Perfect Match: 3.94% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0017 | Train Loss: 0.0654 (Soft Acc: 97.88%) | Val Loss: 0.0603 (Soft Acc: 98.06%) | Perfect Match: 3.96% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0018 | Train Loss: 0.0650 (Soft Acc: 97.89%) | Val Loss: 0.0602 (Soft Acc: 98.06%) | Perfect Match: 3.98% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0019 | Train Loss: 0.0647 (Soft Acc: 97.90%) | Val Loss: 0.0601 (Soft Acc: 98.07%) | Perfect Match: 3.99% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0020 | Train Loss: 0.0644 (Soft Acc: 97.91%) | Val Loss: 0.0600 (Soft Acc: 98.07%) | Perfect Match: 3.98% | LR: 0.001000
Epoch 0021 | Train Loss: 0.0642 (Soft Acc: 97.92%) | Val Loss: 0.0599 (Soft Acc: 98.07%) | Perfect Match: 4.02% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0022 | Train Loss: 0.0639 (Soft Acc: 97.93%) | Val Loss: 0.0599 (Soft Acc: 98.07%) | Perfect Match: 4.04% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0023 | Train Loss: 0.0637 (Soft Acc: 97.94%) | Val Loss: 0.0598 (Soft Acc: 98.08%) | Perfect Match: 4.04% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0024 | Train Loss: 0.0635 (Soft Acc: 97.95%) | Val Loss: 0.0597 (Soft Acc: 98.08%) | Perfect Match: 4.08% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0025 | Train Loss: 0.0633 (Soft Acc: 97.95%) | Val Loss: 0.0596 (Soft Acc: 98.09%) | Perfect Match: 4.10% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0026 | Train Loss: 0.0631 (Soft Acc: 97.96%) | Val Loss: 0.0595 (Soft Acc: 98.09%) | Perfect Match: 4.16% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0027 | Train Loss: 0.0630 (Soft Acc: 97.97%) | Val Loss: 0.0593 (Soft Acc: 98.10%) | Perfect Match: 4.21% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0028 | Train Loss: 0.0628 (Soft Acc: 97.97%) | Val Loss: 0.0592 (Soft Acc: 98.10%) | Perfect Match: 4.27% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0029 | Train Loss: 0.0626 (Soft Acc: 97.98%) | Val Loss: 0.0591 (Soft Acc: 98.11%) | Perfect Match: 4.33% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0030 | Train Loss: 0.0624 (Soft Acc: 97.98%) | Val Loss: 0.0590 (Soft Acc: 98.11%) | Perfect Match: 4.36% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0031 | Train Loss: 0.0623 (Soft Acc: 97.99%) | Val Loss: 0.0588 (Soft Acc: 98.12%) | Perfect Match: 4.40% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0032 | Train Loss: 0.0621 (Soft Acc: 98.00%) | Val Loss: 0.0588 (Soft Acc: 98.12%) | Perfect Match: 4.44% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0033 | Train Loss: 0.0620 (Soft Acc: 98.00%) | Val Loss: 0.0586 (Soft Acc: 98.12%) | Perfect Match: 4.46% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0034 | Train Loss: 0.0618 (Soft Acc: 98.01%) | Val Loss: 0.0586 (Soft Acc: 98.13%) | Perfect Match: 4.47% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0035 | Train Loss: 0.0617 (Soft Acc: 98.01%) | Val Loss: 0.0585 (Soft Acc: 98.13%) | Perfect Match: 4.48% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0036 | Train Loss: 0.0616 (Soft Acc: 98.01%) | Val Loss: 0.0584 (Soft Acc: 98.13%) | Perfect Match: 4.50% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0037 | Train Loss: 0.0615 (Soft Acc: 98.02%) | Val Loss: 0.0584 (Soft Acc: 98.13%) | Perfect Match: 4.52% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0038 | Train Loss: 0.0614 (Soft Acc: 98.02%) | Val Loss: 0.0583 (Soft Acc: 98.13%) | Perfect Match: 4.53% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0039 | Train Loss: 0.0613 (Soft Acc: 98.03%) | Val Loss: 0.0582 (Soft Acc: 98.13%) | Perfect Match: 4.54% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0040 | Train Loss: 0.0611 (Soft Acc: 98.03%) | Val Loss: 0.0582 (Soft Acc: 98.14%) | Perfect Match: 4.54% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0041 | Train Loss: 0.0610 (Soft Acc: 98.03%) | Val Loss: 0.0581 (Soft Acc: 98.14%) | Perfect Match: 4.56% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0042 | Train Loss: 0.0610 (Soft Acc: 98.04%) | Val Loss: 0.0582 (Soft Acc: 98.14%) | Perfect Match: 4.56% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0043 | Train Loss: 0.0609 (Soft Acc: 98.04%) | Val Loss: 0.0581 (Soft Acc: 98.14%) | Perfect Match: 4.58% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0044 | Train Loss: 0.0608 (Soft Acc: 98.04%) | Val Loss: 0.0580 (Soft Acc: 98.14%) | Perfect Match: 4.57% | LR: 0.001000
Epoch 0045 | Train Loss: 0.0607 (Soft Acc: 98.04%) | Val Loss: 0.0579 (Soft Acc: 98.14%) | Perfect Match: 4.59% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0046 | Train Loss: 0.0606 (Soft Acc: 98.05%) | Val Loss: 0.0578 (Soft Acc: 98.14%) | Perfect Match: 4.60% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0047 | Train Loss: 0.0605 (Soft Acc: 98.05%) | Val Loss: 0.0578 (Soft Acc: 98.15%) | Perfect Match: 4.62% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0048 | Train Loss: 0.0604 (Soft Acc: 98.05%) | Val Loss: 0.0578 (Soft Acc: 98.15%) | Perfect Match: 4.61% | LR: 0.001000
Epoch 0049 | Train Loss: 0.0604 (Soft Acc: 98.05%) | Val Loss: 0.0578 (Soft Acc: 98.15%) | Perfect Match: 4.62% | LR: 0.001000
Epoch 0050 | Train Loss: 0.0603 (Soft Acc: 98.06%) | Val Loss: 0.0576 (Soft Acc: 98.15%) | Perfect Match: 4.63% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0051 | Train Loss: 0.0602 (Soft Acc: 98.06%) | Val Loss: 0.0575 (Soft Acc: 98.15%) | Perfect Match: 4.63% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0052 | Train Loss: 0.0601 (Soft Acc: 98.06%) | Val Loss: 0.0575 (Soft Acc: 98.15%) | Perfect Match: 4.64% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0053 | Train Loss: 0.0600 (Soft Acc: 98.06%) | Val Loss: 0.0574 (Soft Acc: 98.15%) | Perfect Match: 4.67% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0054 | Train Loss: 0.0599 (Soft Acc: 98.06%) | Val Loss: 0.0573 (Soft Acc: 98.16%) | Perfect Match: 4.73% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0055 | Train Loss: 0.0599 (Soft Acc: 98.07%) | Val Loss: 0.0572 (Soft Acc: 98.16%) | Perfect Match: 4.79% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0056 | Train Loss: 0.0597 (Soft Acc: 98.07%) | Val Loss: 0.0571 (Soft Acc: 98.16%) | Perfect Match: 4.87% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0057 | Train Loss: 0.0597 (Soft Acc: 98.07%) | Val Loss: 0.0570 (Soft Acc: 98.17%) | Perfect Match: 4.92% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0058 | Train Loss: 0.0596 (Soft Acc: 98.07%) | Val Loss: 0.0569 (Soft Acc: 98.17%) | Perfect Match: 4.96% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0059 | Train Loss: 0.0595 (Soft Acc: 98.07%) | Val Loss: 0.0569 (Soft Acc: 98.17%) | Perfect Match: 4.99% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0060 | Train Loss: 0.0595 (Soft Acc: 98.08%) | Val Loss: 0.0568 (Soft Acc: 98.18%) | Perfect Match: 5.00% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0061 | Train Loss: 0.0594 (Soft Acc: 98.08%) | Val Loss: 0.0568 (Soft Acc: 98.18%) | Perfect Match: 5.05% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0062 | Train Loss: 0.0593 (Soft Acc: 98.08%) | Val Loss: 0.0567 (Soft Acc: 98.18%) | Perfect Match: 5.08% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0063 | Train Loss: 0.0593 (Soft Acc: 98.08%) | Val Loss: 0.0567 (Soft Acc: 98.18%) | Perfect Match: 5.06% | LR: 0.001000
Epoch 0064 | Train Loss: 0.0592 (Soft Acc: 98.08%) | Val Loss: 0.0566 (Soft Acc: 98.19%) | Perfect Match: 5.12% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0065 | Train Loss: 0.0591 (Soft Acc: 98.09%) | Val Loss: 0.0566 (Soft Acc: 98.19%) | Perfect Match: 5.12% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0066 | Train Loss: 0.0591 (Soft Acc: 98.09%) | Val Loss: 0.0566 (Soft Acc: 98.19%) | Perfect Match: 5.13% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0067 | Train Loss: 0.0590 (Soft Acc: 98.09%) | Val Loss: 0.0565 (Soft Acc: 98.19%) | Perfect Match: 5.15% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0068 | Train Loss: 0.0590 (Soft Acc: 98.09%) | Val Loss: 0.0565 (Soft Acc: 98.19%) | Perfect Match: 5.15% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0069 | Train Loss: 0.0589 (Soft Acc: 98.09%) | Val Loss: 0.0565 (Soft Acc: 98.19%) | Perfect Match: 5.14% | LR: 0.001000
Epoch 0070 | Train Loss: 0.0588 (Soft Acc: 98.09%) | Val Loss: 0.0564 (Soft Acc: 98.20%) | Perfect Match: 5.19% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0071 | Train Loss: 0.0588 (Soft Acc: 98.09%) | Val Loss: 0.0564 (Soft Acc: 98.20%) | Perfect Match: 5.22% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0072 | Train Loss: 0.0587 (Soft Acc: 98.10%) | Val Loss: 0.0564 (Soft Acc: 98.20%) | Perfect Match: 5.23% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0073 | Train Loss: 0.0587 (Soft Acc: 98.10%) | Val Loss: 0.0564 (Soft Acc: 98.20%) | Perfect Match: 5.25% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0074 | Train Loss: 0.0586 (Soft Acc: 98.10%) | Val Loss: 0.0563 (Soft Acc: 98.20%) | Perfect Match: 5.28% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0075 | Train Loss: 0.0586 (Soft Acc: 98.10%) | Val Loss: 0.0564 (Soft Acc: 98.20%) | Perfect Match: 5.29% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0076 | Train Loss: 0.0585 (Soft Acc: 98.10%) | Val Loss: 0.0563 (Soft Acc: 98.21%) | Perfect Match: 5.33% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0077 | Train Loss: 0.0585 (Soft Acc: 98.10%) | Val Loss: 0.0562 (Soft Acc: 98.21%) | Perfect Match: 5.33% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0078 | Train Loss: 0.0584 (Soft Acc: 98.10%) | Val Loss: 0.0562 (Soft Acc: 98.21%) | Perfect Match: 5.37% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0079 | Train Loss: 0.0583 (Soft Acc: 98.11%) | Val Loss: 0.0563 (Soft Acc: 98.21%) | Perfect Match: 5.38% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0080 | Train Loss: 0.0583 (Soft Acc: 98.11%) | Val Loss: 0.0562 (Soft Acc: 98.21%) | Perfect Match: 5.43% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0081 | Train Loss: 0.0583 (Soft Acc: 98.11%) | Val Loss: 0.0561 (Soft Acc: 98.22%) | Perfect Match: 5.44% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0082 | Train Loss: 0.0582 (Soft Acc: 98.11%) | Val Loss: 0.0561 (Soft Acc: 98.22%) | Perfect Match: 5.45% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0083 | Train Loss: 0.0582 (Soft Acc: 98.11%) | Val Loss: 0.0561 (Soft Acc: 98.22%) | Perfect Match: 5.48% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0084 | Train Loss: 0.0581 (Soft Acc: 98.11%) | Val Loss: 0.0561 (Soft Acc: 98.22%) | Perfect Match: 5.51% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0085 | Train Loss: 0.0581 (Soft Acc: 98.11%) | Val Loss: 0.0561 (Soft Acc: 98.22%) | Perfect Match: 5.50% | LR: 0.001000
Epoch 0086 | Train Loss: 0.0581 (Soft Acc: 98.11%) | Val Loss: 0.0560 (Soft Acc: 98.22%) | Perfect Match: 5.50% | LR: 0.001000
Epoch 0087 | Train Loss: 0.0580 (Soft Acc: 98.11%) | Val Loss: 0.0561 (Soft Acc: 98.22%) | Perfect Match: 5.53% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0088 | Train Loss: 0.0580 (Soft Acc: 98.11%) | Val Loss: 0.0560 (Soft Acc: 98.22%) | Perfect Match: 5.52% | LR: 0.001000
Epoch 0089 | Train Loss: 0.0579 (Soft Acc: 98.11%) | Val Loss: 0.0561 (Soft Acc: 98.22%) | Perfect Match: 5.54% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0090 | Train Loss: 0.0579 (Soft Acc: 98.12%) | Val Loss: 0.0561 (Soft Acc: 98.23%) | Perfect Match: 5.58% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0091 | Train Loss: 0.0578 (Soft Acc: 98.12%) | Val Loss: 0.0560 (Soft Acc: 98.23%) | Perfect Match: 5.57% | LR: 0.001000
Epoch 0092 | Train Loss: 0.0578 (Soft Acc: 98.12%) | Val Loss: 0.0559 (Soft Acc: 98.23%) | Perfect Match: 5.61% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0093 | Train Loss: 0.0578 (Soft Acc: 98.12%) | Val Loss: 0.0559 (Soft Acc: 98.23%) | Perfect Match: 5.58% | LR: 0.001000
Epoch 0094 | Train Loss: 0.0577 (Soft Acc: 98.12%) | Val Loss: 0.0559 (Soft Acc: 98.23%) | Perfect Match: 5.61% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0095 | Train Loss: 0.0577 (Soft Acc: 98.12%) | Val Loss: 0.0559 (Soft Acc: 98.23%) | Perfect Match: 5.64% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0096 | Train Loss: 0.0576 (Soft Acc: 98.12%) | Val Loss: 0.0560 (Soft Acc: 98.23%) | Perfect Match: 5.63% | LR: 0.001000
Epoch 0097 | Train Loss: 0.0576 (Soft Acc: 98.12%) | Val Loss: 0.0560 (Soft Acc: 98.23%) | Perfect Match: 5.62% | LR: 0.001000
Epoch 0098 | Train Loss: 0.0576 (Soft Acc: 98.12%) | Val Loss: 0.0559 (Soft Acc: 98.23%) | Perfect Match: 5.66% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0099 | Train Loss: 0.0575 (Soft Acc: 98.12%) | Val Loss: 0.0559 (Soft Acc: 98.24%) | Perfect Match: 5.67% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0100 | Train Loss: 0.0575 (Soft Acc: 98.12%) | Val Loss: 0.0558 (Soft Acc: 98.24%) | Perfect Match: 5.67% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0101 | Train Loss: 0.0574 (Soft Acc: 98.12%) | Val Loss: 0.0558 (Soft Acc: 98.24%) | Perfect Match: 5.68% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0102 | Train Loss: 0.0574 (Soft Acc: 98.12%) | Val Loss: 0.0559 (Soft Acc: 98.24%) | Perfect Match: 5.70% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0103 | Train Loss: 0.0574 (Soft Acc: 98.12%) | Val Loss: 0.0559 (Soft Acc: 98.24%) | Perfect Match: 5.70% | LR: 0.001000
Epoch 0104 | Train Loss: 0.0573 (Soft Acc: 98.12%) | Val Loss: 0.0558 (Soft Acc: 98.24%) | Perfect Match: 5.70% | LR: 0.001000
Epoch 0105 | Train Loss: 0.0573 (Soft Acc: 98.12%) | Val Loss: 0.0558 (Soft Acc: 98.24%) | Perfect Match: 5.68% | LR: 0.001000
Epoch 0106 | Train Loss: 0.0573 (Soft Acc: 98.12%) | Val Loss: 0.0558 (Soft Acc: 98.24%) | Perfect Match: 5.69% | LR: 0.001000
Epoch 0107 | Train Loss: 0.0572 (Soft Acc: 98.12%) | Val Loss: 0.0559 (Soft Acc: 98.24%) | Perfect Match: 5.70% | LR: 0.001000
Epoch 0108 | Train Loss: 0.0572 (Soft Acc: 98.12%) | Val Loss: 0.0557 (Soft Acc: 98.24%) | Perfect Match: 5.69% | LR: 0.001000
Epoch 0109 | Train Loss: 0.0571 (Soft Acc: 98.12%) | Val Loss: 0.0558 (Soft Acc: 98.24%) | Perfect Match: 5.71% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0110 | Train Loss: 0.0571 (Soft Acc: 98.13%) | Val Loss: 0.0557 (Soft Acc: 98.24%) | Perfect Match: 5.70% | LR: 0.001000
Epoch 0111 | Train Loss: 0.0571 (Soft Acc: 98.13%) | Val Loss: 0.0558 (Soft Acc: 98.24%) | Perfect Match: 5.74% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0112 | Train Loss: 0.0571 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.74% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0113 | Train Loss: 0.0570 (Soft Acc: 98.13%) | Val Loss: 0.0558 (Soft Acc: 98.24%) | Perfect Match: 5.72% | LR: 0.001000
Epoch 0114 | Train Loss: 0.0570 (Soft Acc: 98.13%) | Val Loss: 0.0557 (Soft Acc: 98.24%) | Perfect Match: 5.73% | LR: 0.001000
Epoch 0115 | Train Loss: 0.0569 (Soft Acc: 98.13%) | Val Loss: 0.0557 (Soft Acc: 98.24%) | Perfect Match: 5.72% | LR: 0.001000
Epoch 0116 | Train Loss: 0.0569 (Soft Acc: 98.13%) | Val Loss: 0.0557 (Soft Acc: 98.24%) | Perfect Match: 5.73% | LR: 0.001000
Epoch 0117 | Train Loss: 0.0569 (Soft Acc: 98.13%) | Val Loss: 0.0557 (Soft Acc: 98.24%) | Perfect Match: 5.74% | LR: 0.001000
Epoch 0118 | Train Loss: 0.0568 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.76% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0119 | Train Loss: 0.0568 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.74% | LR: 0.001000
Epoch 0120 | Train Loss: 0.0568 (Soft Acc: 98.13%) | Val Loss: 0.0557 (Soft Acc: 98.24%) | Perfect Match: 5.75% | LR: 0.001000
Epoch 0121 | Train Loss: 0.0567 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.77% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0122 | Train Loss: 0.0567 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.78% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0123 | Train Loss: 0.0567 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.76% | LR: 0.001000
Epoch 0124 | Train Loss: 0.0566 (Soft Acc: 98.13%) | Val Loss: 0.0557 (Soft Acc: 98.24%) | Perfect Match: 5.77% | LR: 0.001000
Epoch 0125 | Train Loss: 0.0566 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.78% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0126 | Train Loss: 0.0566 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.77% | LR: 0.001000
Epoch 0127 | Train Loss: 0.0565 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0128 | Train Loss: 0.0565 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.25%) | Perfect Match: 5.78% | LR: 0.001000
Epoch 0129 | Train Loss: 0.0565 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0130 | Train Loss: 0.0564 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.76% | LR: 0.001000
Epoch 0131 | Train Loss: 0.0564 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.80% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0132 | Train Loss: 0.0564 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0133 | Train Loss: 0.0563 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0134 | Train Loss: 0.0563 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.80% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0135 | Train Loss: 0.0563 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.82% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0136 | Train Loss: 0.0563 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0137 | Train Loss: 0.0562 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.25%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0138 | Train Loss: 0.0562 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.83% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0139 | Train Loss: 0.0562 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0140 | Train Loss: 0.0561 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0141 | Train Loss: 0.0561 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0142 | Train Loss: 0.0561 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.83% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0143 | Train Loss: 0.0560 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0144 | Train Loss: 0.0560 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0145 | Train Loss: 0.0560 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.83% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0146 | Train Loss: 0.0560 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.84% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0147 | Train Loss: 0.0559 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0148 | Train Loss: 0.0559 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0149 | Train Loss: 0.0559 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0150 | Train Loss: 0.0559 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.84% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0151 | Train Loss: 0.0558 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0152 | Train Loss: 0.0558 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.84% | LR: 0.001000
Epoch 0153 | Train Loss: 0.0558 (Soft Acc: 98.13%) | Val Loss: 0.0556 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0154 | Train Loss: 0.0557 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0155 | Train Loss: 0.0557 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.25%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0156 | Train Loss: 0.0557 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0157 | Train Loss: 0.0556 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0158 | Train Loss: 0.0556 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0159 | Train Loss: 0.0556 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0160 | Train Loss: 0.0556 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0161 | Train Loss: 0.0555 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0162 | Train Loss: 0.0555 (Soft Acc: 98.13%) | Val Loss: 0.0553 (Soft Acc: 98.25%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0163 | Train Loss: 0.0555 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.84% | LR: 0.001000
Epoch 0164 | Train Loss: 0.0555 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0165 | Train Loss: 0.0554 (Soft Acc: 98.13%) | Val Loss: 0.0557 (Soft Acc: 98.24%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0166 | Train Loss: 0.0554 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0167 | Train Loss: 0.0554 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0168 | Train Loss: 0.0554 (Soft Acc: 98.13%) | Val Loss: 0.0554 (Soft Acc: 98.25%) | Perfect Match: 5.84% | LR: 0.001000
Epoch 0169 | Train Loss: 0.0553 (Soft Acc: 98.13%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0170 | Train Loss: 0.0553 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0171 | Train Loss: 0.0553 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0172 | Train Loss: 0.0553 (Soft Acc: 98.14%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0173 | Train Loss: 0.0552 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0174 | Train Loss: 0.0552 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0175 | Train Loss: 0.0552 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0176 | Train Loss: 0.0552 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0177 | Train Loss: 0.0551 (Soft Acc: 98.14%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0178 | Train Loss: 0.0551 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0179 | Train Loss: 0.0551 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0180 | Train Loss: 0.0550 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0181 | Train Loss: 0.0550 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0182 | Train Loss: 0.0550 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0183 | Train Loss: 0.0550 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0184 | Train Loss: 0.0550 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0185 | Train Loss: 0.0549 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0186 | Train Loss: 0.0549 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0187 | Train Loss: 0.0549 (Soft Acc: 98.14%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0188 | Train Loss: 0.0549 (Soft Acc: 98.14%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0189 | Train Loss: 0.0549 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0190 | Train Loss: 0.0548 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0191 | Train Loss: 0.0548 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0192 | Train Loss: 0.0548 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0193 | Train Loss: 0.0547 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0194 | Train Loss: 0.0547 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0195 | Train Loss: 0.0547 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0196 | Train Loss: 0.0547 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0197 | Train Loss: 0.0547 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.77% | LR: 0.001000
Epoch 0198 | Train Loss: 0.0547 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0199 | Train Loss: 0.0546 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0200 | Train Loss: 0.0546 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0201 | Train Loss: 0.0546 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.78% | LR: 0.001000
Epoch 0202 | Train Loss: 0.0546 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0203 | Train Loss: 0.0545 (Soft Acc: 98.14%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0204 | Train Loss: 0.0545 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0205 | Train Loss: 0.0545 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0206 | Train Loss: 0.0545 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0207 | Train Loss: 0.0545 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0208 | Train Loss: 0.0545 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.78% | LR: 0.001000
Epoch 0209 | Train Loss: 0.0544 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0210 | Train Loss: 0.0544 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.24%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0211 | Train Loss: 0.0544 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.23%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0212 | Train Loss: 0.0544 (Soft Acc: 98.14%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0213 | Train Loss: 0.0543 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0214 | Train Loss: 0.0543 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0215 | Train Loss: 0.0543 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0216 | Train Loss: 0.0543 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0217 | Train Loss: 0.0543 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0218 | Train Loss: 0.0542 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0219 | Train Loss: 0.0542 (Soft Acc: 98.14%) | Val Loss: 0.0556 (Soft Acc: 98.23%) | Perfect Match: 5.78% | LR: 0.001000
Epoch 0220 | Train Loss: 0.0542 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0221 | Train Loss: 0.0542 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.23%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0222 | Train Loss: 0.0542 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0223 | Train Loss: 0.0541 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.23%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0224 | Train Loss: 0.0541 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0225 | Train Loss: 0.0541 (Soft Acc: 98.14%) | Val Loss: 0.0555 (Soft Acc: 98.23%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0226 | Train Loss: 0.0541 (Soft Acc: 98.14%) | Val Loss: 0.0554 (Soft Acc: 98.24%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0227 | Train Loss: 0.0541 (Soft Acc: 98.15%) | Val Loss: 0.0555 (Soft Acc: 98.23%) | Perfect Match: 5.78% | LR: 0.001000
Epoch 0228 | Train Loss: 0.0540 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0229 | Train Loss: 0.0540 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0230 | Train Loss: 0.0540 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0231 | Train Loss: 0.0540 (Soft Acc: 98.15%) | Val Loss: 0.0555 (Soft Acc: 98.23%) | Perfect Match: 5.79% | LR: 0.001000
Epoch 0232 | Train Loss: 0.0540 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0233 | Train Loss: 0.0540 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0234 | Train Loss: 0.0539 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0235 | Train Loss: 0.0539 (Soft Acc: 98.15%) | Val Loss: 0.0555 (Soft Acc: 98.23%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0236 | Train Loss: 0.0539 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0237 | Train Loss: 0.0539 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0238 | Train Loss: 0.0539 (Soft Acc: 98.15%) | Val Loss: 0.0555 (Soft Acc: 98.23%) | Perfect Match: 5.78% | LR: 0.001000
Epoch 0239 | Train Loss: 0.0539 (Soft Acc: 98.15%) | Val Loss: 0.0555 (Soft Acc: 98.23%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0240 | Train Loss: 0.0538 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.80% | LR: 0.001000
Epoch 0241 | Train Loss: 0.0538 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.81% | LR: 0.001000
Epoch 0242 | Train Loss: 0.0538 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.83% | LR: 0.001000
Epoch 0243 | Train Loss: 0.0538 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0244 | Train Loss: 0.0537 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.23%) | Perfect Match: 5.85% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0245 | Train Loss: 0.0537 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.23%) | Perfect Match: 5.84% | LR: 0.001000
Epoch 0246 | Train Loss: 0.0537 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.82% | LR: 0.001000
Epoch 0247 | Train Loss: 0.0537 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.88% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0248 | Train Loss: 0.0537 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.85% | LR: 0.001000
Epoch 0249 | Train Loss: 0.0536 (Soft Acc: 98.15%) | Val Loss: 0.0554 (Soft Acc: 98.23%) | Perfect Match: 5.85% | LR: 0.001000
Epoch 0250 | Train Loss: 0.0536 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.23%) | Perfect Match: 5.88% | LR: 0.001000
Epoch 0251 | Train Loss: 0.0536 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.23%) | Perfect Match: 5.89% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0252 | Train Loss: 0.0536 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.23%) | Perfect Match: 5.90% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0253 | Train Loss: 0.0536 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.23%) | Perfect Match: 5.90% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0254 | Train Loss: 0.0535 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.95% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0255 | Train Loss: 0.0535 (Soft Acc: 98.15%) | Val Loss: 0.0552 (Soft Acc: 98.24%) | Perfect Match: 5.92% | LR: 0.001000
Epoch 0256 | Train Loss: 0.0535 (Soft Acc: 98.15%) | Val Loss: 0.0553 (Soft Acc: 98.24%) | Perfect Match: 5.96% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0257 | Train Loss: 0.0535 (Soft Acc: 98.15%) | Val Loss: 0.0552 (Soft Acc: 98.24%) | Perfect Match: 6.00% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0258 | Train Loss: 0.0534 (Soft Acc: 98.16%) | Val Loss: 0.0552 (Soft Acc: 98.24%) | Perfect Match: 6.02% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0259 | Train Loss: 0.0534 (Soft Acc: 98.16%) | Val Loss: 0.0551 (Soft Acc: 98.24%) | Perfect Match: 6.04% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0260 | Train Loss: 0.0534 (Soft Acc: 98.16%) | Val Loss: 0.0551 (Soft Acc: 98.25%) | Perfect Match: 6.10% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0261 | Train Loss: 0.0534 (Soft Acc: 98.16%) | Val Loss: 0.0551 (Soft Acc: 98.25%) | Perfect Match: 6.11% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0262 | Train Loss: 0.0533 (Soft Acc: 98.16%) | Val Loss: 0.0550 (Soft Acc: 98.25%) | Perfect Match: 6.14% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0263 | Train Loss: 0.0533 (Soft Acc: 98.16%) | Val Loss: 0.0550 (Soft Acc: 98.25%) | Perfect Match: 6.15% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0264 | Train Loss: 0.0533 (Soft Acc: 98.16%) | Val Loss: 0.0550 (Soft Acc: 98.26%) | Perfect Match: 6.23% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0265 | Train Loss: 0.0533 (Soft Acc: 98.16%) | Val Loss: 0.0550 (Soft Acc: 98.26%) | Perfect Match: 6.24% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0266 | Train Loss: 0.0533 (Soft Acc: 98.16%) | Val Loss: 0.0549 (Soft Acc: 98.26%) | Perfect Match: 6.25% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0267 | Train Loss: 0.0532 (Soft Acc: 98.16%) | Val Loss: 0.0549 (Soft Acc: 98.26%) | Perfect Match: 6.26% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0268 | Train Loss: 0.0532 (Soft Acc: 98.16%) | Val Loss: 0.0550 (Soft Acc: 98.26%) | Perfect Match: 6.32% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0269 | Train Loss: 0.0532 (Soft Acc: 98.16%) | Val Loss: 0.0549 (Soft Acc: 98.26%) | Perfect Match: 6.30% | LR: 0.001000
Epoch 0270 | Train Loss: 0.0532 (Soft Acc: 98.16%) | Val Loss: 0.0548 (Soft Acc: 98.26%) | Perfect Match: 6.35% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0271 | Train Loss: 0.0531 (Soft Acc: 98.16%) | Val Loss: 0.0548 (Soft Acc: 98.26%) | Perfect Match: 6.36% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0272 | Train Loss: 0.0531 (Soft Acc: 98.16%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.42% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0273 | Train Loss: 0.0531 (Soft Acc: 98.16%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.44% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0274 | Train Loss: 0.0531 (Soft Acc: 98.17%) | Val Loss: 0.0549 (Soft Acc: 98.26%) | Perfect Match: 6.39% | LR: 0.001000
Epoch 0275 | Train Loss: 0.0531 (Soft Acc: 98.17%) | Val Loss: 0.0549 (Soft Acc: 98.26%) | Perfect Match: 6.39% | LR: 0.001000
Epoch 0276 | Train Loss: 0.0530 (Soft Acc: 98.17%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.44% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0277 | Train Loss: 0.0530 (Soft Acc: 98.17%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.45% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0278 | Train Loss: 0.0530 (Soft Acc: 98.17%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.51% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0279 | Train Loss: 0.0530 (Soft Acc: 98.17%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.48% | LR: 0.001000
Epoch 0280 | Train Loss: 0.0530 (Soft Acc: 98.17%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.46% | LR: 0.001000
Epoch 0281 | Train Loss: 0.0529 (Soft Acc: 98.17%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.51% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0282 | Train Loss: 0.0529 (Soft Acc: 98.17%) | Val Loss: 0.0549 (Soft Acc: 98.27%) | Perfect Match: 6.54% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0283 | Train Loss: 0.0529 (Soft Acc: 98.17%) | Val Loss: 0.0547 (Soft Acc: 98.27%) | Perfect Match: 6.53% | LR: 0.001000
Epoch 0284 | Train Loss: 0.0529 (Soft Acc: 98.17%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.54% | LR: 0.001000
Epoch 0285 | Train Loss: 0.0529 (Soft Acc: 98.17%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.54% | LR: 0.001000
Epoch 0286 | Train Loss: 0.0529 (Soft Acc: 98.17%) | Val Loss: 0.0547 (Soft Acc: 98.28%) | Perfect Match: 6.56% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0287 | Train Loss: 0.0529 (Soft Acc: 98.17%) | Val Loss: 0.0547 (Soft Acc: 98.27%) | Perfect Match: 6.58% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0288 | Train Loss: 0.0528 (Soft Acc: 98.17%) | Val Loss: 0.0547 (Soft Acc: 98.27%) | Perfect Match: 6.60% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0289 | Train Loss: 0.0528 (Soft Acc: 98.17%) | Val Loss: 0.0547 (Soft Acc: 98.28%) | Perfect Match: 6.64% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0290 | Train Loss: 0.0528 (Soft Acc: 98.17%) | Val Loss: 0.0546 (Soft Acc: 98.28%) | Perfect Match: 6.59% | LR: 0.001000
Epoch 0291 | Train Loss: 0.0528 (Soft Acc: 98.17%) | Val Loss: 0.0547 (Soft Acc: 98.27%) | Perfect Match: 6.56% | LR: 0.001000
Epoch 0292 | Train Loss: 0.0528 (Soft Acc: 98.17%) | Val Loss: 0.0547 (Soft Acc: 98.28%) | Perfect Match: 6.63% | LR: 0.001000
Epoch 0293 | Train Loss: 0.0527 (Soft Acc: 98.17%) | Val Loss: 0.0548 (Soft Acc: 98.27%) | Perfect Match: 6.65% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0294 | Train Loss: 0.0527 (Soft Acc: 98.17%) | Val Loss: 0.0547 (Soft Acc: 98.28%) | Perfect Match: 6.70% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0295 | Train Loss: 0.0527 (Soft Acc: 98.18%) | Val Loss: 0.0546 (Soft Acc: 98.28%) | Perfect Match: 6.71% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0296 | Train Loss: 0.0527 (Soft Acc: 98.18%) | Val Loss: 0.0547 (Soft Acc: 98.28%) | Perfect Match: 6.70% | LR: 0.001000
Epoch 0297 | Train Loss: 0.0527 (Soft Acc: 98.18%) | Val Loss: 0.0547 (Soft Acc: 98.28%) | Perfect Match: 6.73% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0298 | Train Loss: 0.0527 (Soft Acc: 98.18%) | Val Loss: 0.0546 (Soft Acc: 98.28%) | Perfect Match: 6.75% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0299 | Train Loss: 0.0526 (Soft Acc: 98.18%) | Val Loss: 0.0547 (Soft Acc: 98.28%) | Perfect Match: 6.75% | LR: 0.001000
Epoch 0300 | Train Loss: 0.0526 (Soft Acc: 98.18%) | Val Loss: 0.0546 (Soft Acc: 98.28%) | Perfect Match: 6.77% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0301 | Train Loss: 0.0526 (Soft Acc: 98.18%) | Val Loss: 0.0546 (Soft Acc: 98.28%) | Perfect Match: 6.79% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0302 | Train Loss: 0.0526 (Soft Acc: 98.18%) | Val Loss: 0.0545 (Soft Acc: 98.28%) | Perfect Match: 6.80% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0303 | Train Loss: 0.0526 (Soft Acc: 98.18%) | Val Loss: 0.0545 (Soft Acc: 98.29%) | Perfect Match: 6.82% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0304 | Train Loss: 0.0525 (Soft Acc: 98.18%) | Val Loss: 0.0547 (Soft Acc: 98.28%) | Perfect Match: 6.86% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0305 | Train Loss: 0.0525 (Soft Acc: 98.18%) | Val Loss: 0.0545 (Soft Acc: 98.29%) | Perfect Match: 6.90% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0306 | Train Loss: 0.0525 (Soft Acc: 98.18%) | Val Loss: 0.0547 (Soft Acc: 98.28%) | Perfect Match: 6.85% | LR: 0.001000
Epoch 0307 | Train Loss: 0.0525 (Soft Acc: 98.18%) | Val Loss: 0.0545 (Soft Acc: 98.29%) | Perfect Match: 6.90% | LR: 0.001000
Epoch 0308 | Train Loss: 0.0525 (Soft Acc: 98.18%) | Val Loss: 0.0545 (Soft Acc: 98.29%) | Perfect Match: 6.92% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0309 | Train Loss: 0.0525 (Soft Acc: 98.18%) | Val Loss: 0.0545 (Soft Acc: 98.29%) | Perfect Match: 6.95% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0310 | Train Loss: 0.0524 (Soft Acc: 98.18%) | Val Loss: 0.0544 (Soft Acc: 98.29%) | Perfect Match: 6.99% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0311 | Train Loss: 0.0524 (Soft Acc: 98.18%) | Val Loss: 0.0545 (Soft Acc: 98.29%) | Perfect Match: 6.95% | LR: 0.001000
Epoch 0312 | Train Loss: 0.0524 (Soft Acc: 98.18%) | Val Loss: 0.0546 (Soft Acc: 98.29%) | Perfect Match: 7.00% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0313 | Train Loss: 0.0524 (Soft Acc: 98.18%) | Val Loss: 0.0546 (Soft Acc: 98.29%) | Perfect Match: 7.02% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0314 | Train Loss: 0.0524 (Soft Acc: 98.19%) | Val Loss: 0.0545 (Soft Acc: 98.29%) | Perfect Match: 7.07% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0315 | Train Loss: 0.0524 (Soft Acc: 98.19%) | Val Loss: 0.0544 (Soft Acc: 98.30%) | Perfect Match: 7.07% | LR: 0.001000
Epoch 0316 | Train Loss: 0.0524 (Soft Acc: 98.19%) | Val Loss: 0.0544 (Soft Acc: 98.30%) | Perfect Match: 7.07% | LR: 0.001000
Epoch 0317 | Train Loss: 0.0523 (Soft Acc: 98.19%) | Val Loss: 0.0544 (Soft Acc: 98.30%) | Perfect Match: 7.15% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0318 | Train Loss: 0.0523 (Soft Acc: 98.19%) | Val Loss: 0.0544 (Soft Acc: 98.30%) | Perfect Match: 7.19% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0319 | Train Loss: 0.0523 (Soft Acc: 98.19%) | Val Loss: 0.0545 (Soft Acc: 98.30%) | Perfect Match: 7.19% | LR: 0.001000
Epoch 0320 | Train Loss: 0.0523 (Soft Acc: 98.19%) | Val Loss: 0.0544 (Soft Acc: 98.30%) | Perfect Match: 7.21% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0321 | Train Loss: 0.0523 (Soft Acc: 98.19%) | Val Loss: 0.0545 (Soft Acc: 98.30%) | Perfect Match: 7.18% | LR: 0.001000
Epoch 0322 | Train Loss: 0.0522 (Soft Acc: 98.19%) | Val Loss: 0.0544 (Soft Acc: 98.30%) | Perfect Match: 7.18% | LR: 0.001000
Epoch 0323 | Train Loss: 0.0522 (Soft Acc: 98.19%) | Val Loss: 0.0543 (Soft Acc: 98.31%) | Perfect Match: 7.26% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0324 | Train Loss: 0.0522 (Soft Acc: 98.19%) | Val Loss: 0.0543 (Soft Acc: 98.31%) | Perfect Match: 7.28% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0325 | Train Loss: 0.0522 (Soft Acc: 98.19%) | Val Loss: 0.0543 (Soft Acc: 98.31%) | Perfect Match: 7.30% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0326 | Train Loss: 0.0522 (Soft Acc: 98.19%) | Val Loss: 0.0543 (Soft Acc: 98.31%) | Perfect Match: 7.26% | LR: 0.001000
Epoch 0327 | Train Loss: 0.0522 (Soft Acc: 98.19%) | Val Loss: 0.0542 (Soft Acc: 98.31%) | Perfect Match: 7.34% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0328 | Train Loss: 0.0521 (Soft Acc: 98.19%) | Val Loss: 0.0542 (Soft Acc: 98.31%) | Perfect Match: 7.31% | LR: 0.001000
Epoch 0329 | Train Loss: 0.0521 (Soft Acc: 98.20%) | Val Loss: 0.0542 (Soft Acc: 98.31%) | Perfect Match: 7.36% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0330 | Train Loss: 0.0521 (Soft Acc: 98.20%) | Val Loss: 0.0542 (Soft Acc: 98.32%) | Perfect Match: 7.45% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0331 | Train Loss: 0.0521 (Soft Acc: 98.20%) | Val Loss: 0.0542 (Soft Acc: 98.32%) | Perfect Match: 7.46% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0332 | Train Loss: 0.0521 (Soft Acc: 98.20%) | Val Loss: 0.0541 (Soft Acc: 98.32%) | Perfect Match: 7.49% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0333 | Train Loss: 0.0521 (Soft Acc: 98.20%) | Val Loss: 0.0542 (Soft Acc: 98.32%) | Perfect Match: 7.46% | LR: 0.001000
Epoch 0334 | Train Loss: 0.0520 (Soft Acc: 98.20%) | Val Loss: 0.0542 (Soft Acc: 98.32%) | Perfect Match: 7.49% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0335 | Train Loss: 0.0520 (Soft Acc: 98.20%) | Val Loss: 0.0541 (Soft Acc: 98.32%) | Perfect Match: 7.56% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0336 | Train Loss: 0.0520 (Soft Acc: 98.20%) | Val Loss: 0.0540 (Soft Acc: 98.33%) | Perfect Match: 7.55% | LR: 0.001000
Epoch 0337 | Train Loss: 0.0520 (Soft Acc: 98.20%) | Val Loss: 0.0541 (Soft Acc: 98.33%) | Perfect Match: 7.57% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0338 | Train Loss: 0.0520 (Soft Acc: 98.20%) | Val Loss: 0.0540 (Soft Acc: 98.33%) | Perfect Match: 7.61% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0339 | Train Loss: 0.0519 (Soft Acc: 98.20%) | Val Loss: 0.0540 (Soft Acc: 98.33%) | Perfect Match: 7.68% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0340 | Train Loss: 0.0519 (Soft Acc: 98.20%) | Val Loss: 0.0540 (Soft Acc: 98.33%) | Perfect Match: 7.69% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0341 | Train Loss: 0.0519 (Soft Acc: 98.21%) | Val Loss: 0.0540 (Soft Acc: 98.33%) | Perfect Match: 7.68% | LR: 0.001000
Epoch 0342 | Train Loss: 0.0519 (Soft Acc: 98.21%) | Val Loss: 0.0539 (Soft Acc: 98.34%) | Perfect Match: 7.72% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0343 | Train Loss: 0.0519 (Soft Acc: 98.21%) | Val Loss: 0.0541 (Soft Acc: 98.33%) | Perfect Match: 7.72% | LR: 0.001000
Epoch 0344 | Train Loss: 0.0519 (Soft Acc: 98.21%) | Val Loss: 0.0539 (Soft Acc: 98.34%) | Perfect Match: 7.83% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0345 | Train Loss: 0.0518 (Soft Acc: 98.21%) | Val Loss: 0.0539 (Soft Acc: 98.34%) | Perfect Match: 7.81% | LR: 0.001000
Epoch 0346 | Train Loss: 0.0518 (Soft Acc: 98.21%) | Val Loss: 0.0538 (Soft Acc: 98.34%) | Perfect Match: 7.86% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0347 | Train Loss: 0.0518 (Soft Acc: 98.21%) | Val Loss: 0.0538 (Soft Acc: 98.34%) | Perfect Match: 7.83% | LR: 0.001000
Epoch 0348 | Train Loss: 0.0518 (Soft Acc: 98.21%) | Val Loss: 0.0539 (Soft Acc: 98.34%) | Perfect Match: 7.82% | LR: 0.001000
Epoch 0349 | Train Loss: 0.0518 (Soft Acc: 98.21%) | Val Loss: 0.0538 (Soft Acc: 98.34%) | Perfect Match: 7.89% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0350 | Train Loss: 0.0518 (Soft Acc: 98.21%) | Val Loss: 0.0537 (Soft Acc: 98.35%) | Perfect Match: 7.91% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0351 | Train Loss: 0.0517 (Soft Acc: 98.21%) | Val Loss: 0.0537 (Soft Acc: 98.35%) | Perfect Match: 7.96% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0352 | Train Loss: 0.0517 (Soft Acc: 98.21%) | Val Loss: 0.0539 (Soft Acc: 98.34%) | Perfect Match: 7.91% | LR: 0.001000
Epoch 0353 | Train Loss: 0.0517 (Soft Acc: 98.21%) | Val Loss: 0.0538 (Soft Acc: 98.35%) | Perfect Match: 7.97% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0354 | Train Loss: 0.0517 (Soft Acc: 98.21%) | Val Loss: 0.0537 (Soft Acc: 98.35%) | Perfect Match: 7.95% | LR: 0.001000
Epoch 0355 | Train Loss: 0.0517 (Soft Acc: 98.21%) | Val Loss: 0.0538 (Soft Acc: 98.35%) | Perfect Match: 7.98% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0356 | Train Loss: 0.0516 (Soft Acc: 98.22%) | Val Loss: 0.0537 (Soft Acc: 98.35%) | Perfect Match: 7.97% | LR: 0.001000
Epoch 0357 | Train Loss: 0.0516 (Soft Acc: 98.22%) | Val Loss: 0.0537 (Soft Acc: 98.35%) | Perfect Match: 7.95% | LR: 0.001000
Epoch 0358 | Train Loss: 0.0516 (Soft Acc: 98.22%) | Val Loss: 0.0537 (Soft Acc: 98.35%) | Perfect Match: 7.96% | LR: 0.001000
Epoch 0359 | Train Loss: 0.0516 (Soft Acc: 98.22%) | Val Loss: 0.0537 (Soft Acc: 98.35%) | Perfect Match: 8.00% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0360 | Train Loss: 0.0516 (Soft Acc: 98.22%) | Val Loss: 0.0536 (Soft Acc: 98.35%) | Perfect Match: 8.05% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0361 | Train Loss: 0.0516 (Soft Acc: 98.22%) | Val Loss: 0.0537 (Soft Acc: 98.35%) | Perfect Match: 8.07% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0362 | Train Loss: 0.0516 (Soft Acc: 98.22%) | Val Loss: 0.0537 (Soft Acc: 98.36%) | Perfect Match: 8.11% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0363 | Train Loss: 0.0516 (Soft Acc: 98.22%) | Val Loss: 0.0537 (Soft Acc: 98.36%) | Perfect Match: 8.13% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0364 | Train Loss: 0.0515 (Soft Acc: 98.22%) | Val Loss: 0.0536 (Soft Acc: 98.36%) | Perfect Match: 8.08% | LR: 0.001000
Epoch 0365 | Train Loss: 0.0515 (Soft Acc: 98.22%) | Val Loss: 0.0536 (Soft Acc: 98.36%) | Perfect Match: 8.16% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0366 | Train Loss: 0.0515 (Soft Acc: 98.22%) | Val Loss: 0.0536 (Soft Acc: 98.36%) | Perfect Match: 8.13% | LR: 0.001000
Epoch 0367 | Train Loss: 0.0515 (Soft Acc: 98.22%) | Val Loss: 0.0536 (Soft Acc: 98.36%) | Perfect Match: 8.15% | LR: 0.001000
Epoch 0368 | Train Loss: 0.0515 (Soft Acc: 98.22%) | Val Loss: 0.0536 (Soft Acc: 98.36%) | Perfect Match: 8.11% | LR: 0.001000
Epoch 0369 | Train Loss: 0.0515 (Soft Acc: 98.22%) | Val Loss: 0.0536 (Soft Acc: 98.36%) | Perfect Match: 8.14% | LR: 0.001000
Epoch 0370 | Train Loss: 0.0514 (Soft Acc: 98.22%) | Val Loss: 0.0535 (Soft Acc: 98.36%) | Perfect Match: 8.17% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0371 | Train Loss: 0.0514 (Soft Acc: 98.23%) | Val Loss: 0.0536 (Soft Acc: 98.36%) | Perfect Match: 8.16% | LR: 0.001000
Epoch 0372 | Train Loss: 0.0514 (Soft Acc: 98.23%) | Val Loss: 0.0536 (Soft Acc: 98.36%) | Perfect Match: 8.13% | LR: 0.001000
Epoch 0373 | Train Loss: 0.0514 (Soft Acc: 98.23%) | Val Loss: 0.0537 (Soft Acc: 98.36%) | Perfect Match: 8.18% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0374 | Train Loss: 0.0514 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.36%) | Perfect Match: 8.20% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0375 | Train Loss: 0.0514 (Soft Acc: 98.23%) | Val Loss: 0.0535 (Soft Acc: 98.36%) | Perfect Match: 8.20% | LR: 0.001000
Epoch 0376 | Train Loss: 0.0514 (Soft Acc: 98.23%) | Val Loss: 0.0537 (Soft Acc: 98.36%) | Perfect Match: 8.16% | LR: 0.001000
Epoch 0377 | Train Loss: 0.0513 (Soft Acc: 98.23%) | Val Loss: 0.0535 (Soft Acc: 98.36%) | Perfect Match: 8.17% | LR: 0.001000
Epoch 0378 | Train Loss: 0.0513 (Soft Acc: 98.23%) | Val Loss: 0.0535 (Soft Acc: 98.36%) | Perfect Match: 8.23% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0379 | Train Loss: 0.0513 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.37%) | Perfect Match: 8.24% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0380 | Train Loss: 0.0513 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.36%) | Perfect Match: 8.21% | LR: 0.001000
Epoch 0381 | Train Loss: 0.0513 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.36%) | Perfect Match: 8.23% | LR: 0.001000
Epoch 0382 | Train Loss: 0.0513 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.36%) | Perfect Match: 8.21% | LR: 0.001000
Epoch 0383 | Train Loss: 0.0512 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.36%) | Perfect Match: 8.21% | LR: 0.001000
Epoch 0384 | Train Loss: 0.0512 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.36%) | Perfect Match: 8.21% | LR: 0.001000
Epoch 0385 | Train Loss: 0.0512 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.36%) | Perfect Match: 8.26% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0386 | Train Loss: 0.0512 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.36%) | Perfect Match: 8.23% | LR: 0.001000
Epoch 0387 | Train Loss: 0.0512 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.37%) | Perfect Match: 8.29% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0388 | Train Loss: 0.0512 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.37%) | Perfect Match: 8.30% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0389 | Train Loss: 0.0512 (Soft Acc: 98.23%) | Val Loss: 0.0534 (Soft Acc: 98.37%) | Perfect Match: 8.29% | LR: 0.001000
Epoch 0390 | Train Loss: 0.0511 (Soft Acc: 98.24%) | Val Loss: 0.0534 (Soft Acc: 98.37%) | Perfect Match: 8.32% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0391 | Train Loss: 0.0512 (Soft Acc: 98.24%) | Val Loss: 0.0534 (Soft Acc: 98.36%) | Perfect Match: 8.25% | LR: 0.001000
Epoch 0392 | Train Loss: 0.0511 (Soft Acc: 98.24%) | Val Loss: 0.0534 (Soft Acc: 98.37%) | Perfect Match: 8.32% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0393 | Train Loss: 0.0511 (Soft Acc: 98.24%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.33% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0394 | Train Loss: 0.0511 (Soft Acc: 98.24%) | Val Loss: 0.0534 (Soft Acc: 98.37%) | Perfect Match: 8.31% | LR: 0.001000
Epoch 0395 | Train Loss: 0.0511 (Soft Acc: 98.24%) | Val Loss: 0.0534 (Soft Acc: 98.37%) | Perfect Match: 8.34% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0396 | Train Loss: 0.0511 (Soft Acc: 98.24%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.37% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0397 | Train Loss: 0.0511 (Soft Acc: 98.24%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.33% | LR: 0.001000
Epoch 0398 | Train Loss: 0.0511 (Soft Acc: 98.24%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.35% | LR: 0.001000
Epoch 0399 | Train Loss: 0.0510 (Soft Acc: 98.24%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.31% | LR: 0.001000
Epoch 0400 | Train Loss: 0.0510 (Soft Acc: 98.24%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.32% | LR: 0.001000
Epoch 0401 | Train Loss: 0.0510 (Soft Acc: 98.24%) | Val Loss: 0.0534 (Soft Acc: 98.37%) | Perfect Match: 8.30% | LR: 0.001000
Epoch 0402 | Train Loss: 0.0510 (Soft Acc: 98.24%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.35% | LR: 0.001000
Epoch 0403 | Train Loss: 0.0510 (Soft Acc: 98.24%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.36% | LR: 0.001000
Epoch 0404 | Train Loss: 0.0510 (Soft Acc: 98.24%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.39% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0405 | Train Loss: 0.0510 (Soft Acc: 98.24%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.40% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0406 | Train Loss: 0.0509 (Soft Acc: 98.24%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.38% | LR: 0.001000
Epoch 0407 | Train Loss: 0.0509 (Soft Acc: 98.25%) | Val Loss: 0.0531 (Soft Acc: 98.37%) | Perfect Match: 8.41% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0408 | Train Loss: 0.0509 (Soft Acc: 98.25%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.35% | LR: 0.001000
Epoch 0409 | Train Loss: 0.0509 (Soft Acc: 98.25%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.41% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0410 | Train Loss: 0.0509 (Soft Acc: 98.25%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.44% | LR: 0.001000
  --> 🎉 New best perfect match acc! Saved weights to 'best_modulo_model.pt'
Epoch 0411 | Train Loss: 0.0509 (Soft Acc: 98.25%) | Val Loss: 0.0533 (Soft Acc: 98.37%) | Perfect Match: 8.36% | LR: 0.001000
Epoch 0412 | Train Loss: 0.0509 (Soft Acc: 98.25%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.38% | LR: 0.001000
Epoch 0413 | Train Loss: 0.0508 (Soft Acc: 98.25%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.44% | LR: 0.001000
Epoch 0414 | Train Loss: 0.0508 (Soft Acc: 98.25%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.38% | LR: 0.001000
Epoch 0415 | Train Loss: 0.0508 (Soft Acc: 98.25%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.42% | LR: 0.001000
Epoch 0416 | Train Loss: 0.0508 (Soft Acc: 98.25%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.43% | LR: 0.001000
Epoch 0417 | Train Loss: 0.0508 (Soft Acc: 98.25%) | Val Loss: 0.0532 (Soft Acc: 98.37%) | Perfect Match: 8.43% | LR: 0.001000
"""

def parse_and_plot(text):
    epochs = []
    train_losses = []
    val_losses = []
    train_soft_accs = []
    val_soft_accs = []
    perfect_matches = []

    # Regex designed to capture Train/Val Loss, Train/Val Soft Accuracy, and Perfect Match
    pattern = re.compile(
        r"Epoch\s+(\d+)\s*\|\s*"
        r"Train Loss:\s*([\d.]+)\s*\(Soft Acc:\s*([\d.]+)%\)\s*\|\s*"
        r"Val Loss:\s*([\d.]+)\s*\(Soft Acc:\s*([\d.]+)%\)\s*\|\s*"
        r"Perfect Match:\s*([\d.]+)%"
    )

    for line in text.strip().split("\n"):
        match = pattern.search(line)
        if match:
            epochs.append(int(match.group(1)))
            train_losses.append(float(match.group(2)))
            train_soft_accs.append(float(match.group(3)))
            val_losses.append(float(match.group(4)))
            val_soft_accs.append(float(match.group(5)))
            perfect_matches.append(float(match.group(6)))

    if not epochs:
        print("No matches found! Please verify that your log snippet matches the regex format.")
        return

    fig, ax1 = plt.subplots(figsize=(11, 7))

    # --- Left Y-Axis: Losses ---
    color_train_loss = '#1f77b4'  # Blue
    color_val_loss = '#ff7f0e'    # Orange
    
    ax1.set_xlabel('Epoch', fontweight='bold')
    ax1.set_ylabel('Loss', color='black', fontweight='bold')
    
    line1 = ax1.plot(epochs, train_losses, color=color_train_loss, marker='o', label='Train Loss', linewidth=2)
    line2 = ax1.plot(epochs, val_losses, color=color_val_loss, marker='s', label='Val Loss', linewidth=2)
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.grid(True, linestyle='--', alpha=0.6)

    # --- Right Y-Axis: Accuracies (%) ---
    ax2 = ax1.twinx()  
    
    # Let's use shades of green/teal for accuracy metrics
    color_train_soft = '#34a853'   # Soft Green
    color_val_soft = '#12c2e9'     # Cyan/Teal
    color_perfect = '#8e2de2'      # Vibrant Purple for the ultimate prize: Perfect Match
    
    ax2.set_ylabel('Accuracy (%)', color='black', fontweight='bold')
    
    # Soft Accuracies (Dashed to signify intermediate step)
    line3 = ax2.plot(epochs, train_soft_accs, color=color_train_soft, linestyle='--', marker='x', label='Train Soft Acc (%)', alpha=0.7)
    line4 = ax2.plot(epochs, val_soft_accs, color=color_val_soft, linestyle='--', marker='+', label='Val Soft Acc (%)', alpha=0.7)
    
    # Perfect Match (Solid thick line)
    line5 = ax2.plot(epochs, perfect_matches, color=color_perfect, marker='^', label='Perfect Match (%)', linewidth=2.5)
    
    ax2.tick_params(axis='y', labelcolor='black')

    # Combined Legend
    lines = line1 + line2 + line3 + line4 + line5
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center left', bbox_to_anchor=(0.02, 0.5))  # Moved to prevent covering lines

    plt.title('Modulo Net VQ Training Performance History (with Soft Accuracies)', fontsize=13, fontweight='bold', pad=15)
    fig.tight_layout()
    
    plt.show()

if __name__ == "__main__":
    parse_and_plot(log_data)
import tensorflow as tf
import tensorflow.keras.layers as kl
import tensorflow.keras.regularizers as kr

class Bottleneck(tf.keras.Model):
    def __init__(self, in_channels, out_channels):
        super().__init__()

        self.bn1 = kl.BatchNormalization()
        self.relu = kl.Activation(tf.nn.relu)
        self.den1 = kl.Dense(out_channels)

        self.bn2 = kl.BatchNormalization()
        self.den2 = kl.Dense(out_channels)

        self.bn3 = kl.BatchNormalization()
        self.den3 = kl.Dense(out_channels)

        self.shortcut = self._resblock(in_channels, out_channels)
        self.add = kl.Add()
        self.dropout = kl.Dropout(0.3)

    # Shortcut Connection
    def _resblock(self, in_channels, out_channels):

        if in_channels != out_channels:
            self.bn_res1 = kl.BatchNormalization()
            self.den_res1 = kl.Dense(out_channels, use_bias=False)
            return  self.den_res1 #lambda x : self.add([x, x])
        else:
            return lambda x : x

    def call(self, x):
        
        out = self.den1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.den2(out)
        out = self.bn2(out)
        out = self.relu(out)
        
        out = self.den3(out)
        out = self.bn3(out)
        out = self.relu(out)
        out = self.dropout(out)

        identity = self.shortcut(x)
        #if identity.shape[1] != out.shape[1]:
        #    identity = tf.concat([identity, identity], -1)
        out = self.add([out, identity])
        out = self.relu(out)

        return out

# ResNet50(Pre Activation)
class ResNet(tf.keras.Model):
    def __init__(self, input_dim, output_dim):
        super().__init__()

        self._layers = [
            kl.Dense(100, kernel_regularizer = kr.l2(0.001), use_bias=False),

            [
                Bottleneck(100, 100) for _ in range(2)
            ],
            kl.Dense(200, kernel_regularizer = kr.l2(0.001), use_bias=False),
            [
                Bottleneck(200, 200) for _ in range(2)
            ],
             kl.Dense(400, kernel_regularizer = kr.l2(0.001), use_bias=False),
            [
                Bottleneck(400, 400) for _ in range(4)
            ],
             kl.Dense(800, kernel_regularizer = kr.l2(0.001), use_bias=False),
            [
                Bottleneck(800, 800) for _ in range(4)
            ],
            kl.Dense(output_dim, activation="softmax")
        ]

    def call(self, x):
        for layer in self._layers:

            if isinstance(layer, list):
                for l in layer:
                    x = l(x)
            else:
                x = layer(x)

        return x

# 学習
def ResRace(input_dim, output_dim):
    model = ResNet(input_dim, output_dim)
    model.build(input_shape=(None, input_dim))
    opt = tf.keras.optimizers.SGD(momentum = 0.9)
    model.compile(loss = tf.keras.losses.categorical_crossentropy, optimazer = "adam", metrics = ['accuracy'])
    
    return model

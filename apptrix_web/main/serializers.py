from rest_framework import serializers

from .models import MyUser, Likes


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'image', 'email', 'first_name', 'last_name', 'gender', 'password', 'date_joined']

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)

    # def update(self, instance, validated_data):
        # user = super().update(instance, validated_data)
        # image = validated_data.get('image')
        # if image is not None:
        #     paste_watermark(user.image.path)
        # return user
        # pass

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password')
        ret['registration_date'] = ret.pop('date_joined')
        ret['gender'] = instance.get_gender_display()
        return ret


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['receiver_id', 'date']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        receiver_id = ret.pop('receiver_id')
        if receiver_id:
            ret['user'] = str(MyUser.objects.get(pk=receiver_id))
            ret.move_to_end('date')
        return ret

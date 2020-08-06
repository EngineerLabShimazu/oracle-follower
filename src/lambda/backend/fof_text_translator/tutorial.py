text_map = {
    'TUTORIAL_LAUNCH': """
    <speak>
    <p>
        <prosody pitch="x-high">
            いよいよ今日からだねっ！
        </prosody>
    </p>
    <p>
        <prosody pitch="x-high">
            憧れの<sub alias="さいこうしん">最高神</sub>様に、私たちもなれるかなぁ、、、
        </prosody>
    </p>
    <p>
        <prosody pitch="x-high">
            神として徳を積み、信者が集まると、神としてのランクが上がるんだよねっ！
        </prosody>
    </p>
    <p>
        <prosody pitch="x-high">
            あ！<sub alias="さいこうしん">最高神</sub>様だっ！
        </prosody>
    </p>
    <break time="1s"/>
    <p>
        <voice name="Takumi">
            <prosody pitch="x-low">
            初めまして、ユーザーさん。あなたも徳を積んで100年ですね。今日から勇者を育て、世界を導く責務を与えます。
            あなたが導く勇者の様子を見てみましょうか。
            </prosody>
        </voice>
    </p>
    <break time="1s"/>
    <p>
        <voice name="Takumi">
            教えてください、我が主よ、、、。
            <break time="1s" />
            妹の病を直すには一体、どうすれば、、、
        </voice>
    </p>
    <break time="1s"/>
    <p>
        <voice name="Takumi">
            <prosody pitch="x-low">
            勇者の妹に危機が迫っているようですね。勇者にお告げを与え、救いましょう。今回は「ブルードレスへ向かえ」と言いなさい。
            </prosody>
        </voice>
    </p>
    </speak>
    """,
    'TUTORIAL_SALVATION': """
    <speak>
    <p>
        <voice name="Takumi">
            この声は、、、
            <break time="1s" />
            私をお導きくださるのですね！かしこまりました！ブルードレスへ向かいます！
        </voice>
        <audio src="soundbank://soundlibrary/human/amzn_sfx_person_running_01"/>
    </p>
    <p>
        <voice name="Takumi">
            <prosody pitch="x-low">
            今回は特別に、勇者の世界の時間を<sub alias="いちにち">１日</sub>経過させます。
            </prosody>
        </voice>
        <audio src="soundbank://soundlibrary/magic_spells/magic_spells_15"/>
        <break time="1s" />
    </p>
    <p>
        <audio src="soundbank://soundlibrary/animals/amzn_sfx_bird_chickadee_chirps_01"/>
        <voice name="Takumi">
            神様、昨日はお告げを頂き、ありがとうございました。妹の病を治せる薬を入手することができました。
        </voice>
    </p>
    <p>
        <voice name="Takumi">
            <prosody pitch="x-low">
            あなたのお告げで、勇者の妹が救われました。この調子で、さらなる徳を積み重ねなさい。
            </prosody>
        </voice>
    </p>
    <p>
        <voice name="Takumi">
            <prosody pitch="x-low">
                さすれば、あなたも<sub alias="さいこうしん">最高神</sub>へと近づくでしょう。
            </prosody>
        </voice>
    </p>
    <p>
        <prosody pitch="x-high">
            よし、勇者をいろんな土地へと導いて、人々を救わせよう！
        </prosody>
    </p>
    <p>
        <voice name="Takumi">
            神様、迷える人のもとへお導きください。
            次はブルードレスとマゼンタコートのどちらへ向かえばよろしいでしょうか。
        </voice>
    </p>
    </speak>
    """,
    'TUTORIAL_SALVATION_ASK': """
    <speak>
    <p>
        <voice name="Takumi">
            <prosody pitch="x-low">
                勇者の妹に危機が迫っているようですね。
                勇者にお告げを与え、救いましょう。
                今回は「ブルードレスへ向かえ」と言いなさい。
            </prosody>
        </voice>
    </p>
    </speak>
    """,
    'TUTORIAL_SEND_OUT': """
    <speak>
        <p>
            <voice name="Takumi">
                {destination} へ行くのですね!ありがとうございます!行ってきます！
            </voice>
            <audio src="soundbank://soundlibrary/human/amzn_sfx_person_running_01"/>
        </p>
        <break time="1s"/>
        <p>
            <prosody pitch="x-high">
                素敵な勇者君ねっ！私も、担当の勇者の様子をみてくるわっ！じゃあ、お互い <say-as interpret-as="interjection">がんばりましょう</say-as>
            </prosody>
        </p>
        <break time="1s"/>
    </speak>
    """,
    'TUTORIAL_SEND_OUT_ASK': """
    <speak>
    <p>
        <voice name="Takumi">
            神様、迷える人のもとへお導きください。
            次はブルードレスとマゼンタコートのどちらへ向かえばよろしいでしょうか。
        </voice>
    </p>
    </speak>
    """
}

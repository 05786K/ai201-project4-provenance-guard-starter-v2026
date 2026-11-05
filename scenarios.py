# The appeal path (criterion 4) can't be tested by sending text alone: it needs
# a submission first and then an appeal against the content_id that came back.
# run_eval.py only sends to /submit, so that scenario below just supplies the
# text to submit; the appeal itself (200 + under_review, and 404 for an unknown
# content_id) is tested by hand, and the write-up should say so.

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": [
            """The tutorial is about GIMP which is an image editing application. It teaches the readers on how to use GIMP to do basic tasks. Yes, it does tell the readers about what GIMP is and what it does. It is explained well. I think anyone with no tech background can understand what is written there about GIMP. I think it is well organized and is tailored for beginner users.""",

            """The formatting and design is great. I didn’t see anything confusing. I like how it explained the user interface first and then went onto describing how users can work on a project and save their work. The author does well job on explaining the windows Modes. It would have been better if the author had included a snapshot of the single window enable/disable settings. I don’t think the author make any assumption because the document explains everything mentioned on the title page. It has the descriptions along with visuals.""",

            """The author explains on the first page what GIMP tutorial is about. It does a good job explaining them as well. The audience will have a basic understanding of what GIMP is and what its used for. They can always refer back to the tutorial for anything in particular. The tutorial flows great. I didn’t notice any redundant steps or written portions.""",

            """Adding an image for the windows enable/disable settings would make it better. I suggest adding a brief description for each menu tab listed in “Workspace Element” sections would improve the tutorial. The paragraphs is organized well. They flow and make sense. The conclusion briefly explained everything covered in the tutorial. Steps are denoted using numbers and bullets. They are clear and flow great. The figures were used appropriately and they added more meaning to the text.""",

            """The tutorial is about how a user can use Gmail and its email sorting features. The author gave background on gmail and described what it does and what its used for. I found it hard to follow this tutorial because the images used in the tutorial are blurry and also there’s so much text to read. Blurry images and crammed up text are the two formatting/layout issues. The tutorial does a good job on explaining the home screen, but it’s a little over-detailed.""",

            """The author probably assumed that the readers need to know every bit of a feature in gmail. Yes, the author explained on the first page that this tutorial is about using Gmail sorting feature. The main takeaways from this tutorial is the use of labels to sort emails. I felt like there were some redundant statements throughout the tutorial. I think some descripts could be written in short and simple ways.""",

            """Using high resolution images so the texts are more visible. Rephrasing some sentences so they are a little bit smaller would make some stuff interesting to the reader. The paragraphs have a purpose and are explained well. But, some are really detailed. I don’t think people need that much information. The steps are described using numbered lines. Each step has an image too. The images are blurry tho. The figure are used appropriately and have captions as well.""",

            """The tutorial is about using youTube. The author explains how a user can register, watch videos and use the system. The author gives enough background on youTube, so the audience know what it is and how they can use. The tutorial is easy to follow there different colors are used for titles and paragraphs. There is some spacing between lines which make it easier to follow. I don’t think there is any formatting/layout issue with this tutorial.""",

            """The author does a good job on explaining each feature the app has. The feature is described and referenced using visuals. I think the author assumed the users are beginner because the tutorial is easy to understand. The author did not mention anything about what the tutorial will teach the audience in the intro paragraph. So, the intro paragraph in the first is missing that information. The audience takeaways would be using some youTube features.""",

            """I didn’t notice any redundancies. The intro does not mention anything about the takeaways of this tutorial is, so the author needs to add that. I think the only missing part is the intro to get fixed. The paragraphs have a purpose and are clear. The closing paragraph summarized the stuff explained in the tutorial. Steps are presented with numbers lines. Different colors are used for titles and sentences. The figures are used appropriately and don’t need any improvement."""
        ],
    },

    {
        "name": "score spread",
        "criterion": 2,
        "texts": [
            # Clearly AI-generated examples
            """Artificial intelligence is transforming modern industries by improving efficiency, supporting decision-making, and automating repetitive tasks. Organizations increasingly rely on data-driven systems to streamline operations and deliver better services. As these technologies continue to develop, businesses must consider accuracy, privacy, and responsible implementation.""",

            """Climate change is one of the most significant challenges facing the world today. Rising temperatures, changing weather patterns, and increasing sea levels affect ecosystems and communities. Governments, businesses, and individuals must work together to reduce emissions and develop sustainable solutions for the future.""",

            """Technology plays an important role in modern education. Online learning platforms provide students with access to educational resources regardless of their location. These tools also allow teachers to organize lessons, monitor progress, and communicate with students more efficiently.""",

            """Maintaining a healthy lifestyle requires a combination of regular physical activity, balanced nutrition, and adequate sleep. Small daily habits can contribute to long-term improvements in physical and mental well-being. Consistency is important when developing routines that support overall health.""",

            """Cybersecurity has become increasingly important as organizations store and process larger amounts of digital information. Strong passwords, software updates, access controls, and employee training can reduce security risks. Organizations should regularly review their security practices to protect sensitive information.""",

            # Clearly human-written examples from your own writing
            """The tutorial is about GIMP which is an image editing application. It teaches the readers on how to use GIMP to do basic tasks. Yes, it does tell the readers about what GIMP is and what it does. It is explained well. I think anyone with no tech background can understand what is written there about GIMP.""",

            """The formatting and design is great. I didn’t see anything confusing. I like how it explained the user interface first and then went onto describing how users can work on a project and save their work.""",

            """The tutorial is about how a user can use Gmail and its email sorting features. The author gave background on gmail and described what it does and what its used for. I found it hard to follow this tutorial because the images used in the tutorial are blurry and also there’s so much text to read.""",

            """The tutorial is about using youTube. The author explains how a user can register, watch videos and use the system. The author gives enough background on youTube, so the audience know what it is and how they can use.""",

            """I think the author assumed the users are beginner because the tutorial is easy to understand. The author did not mention anything about what the tutorial will teach the audience in the intro paragraph. So, the intro paragraph in the first is missing that information."""
        ],
    },

    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            """Artificial intelligence is transforming modern industries by improving efficiency, supporting decision-making, and automating repetitive tasks. Organizations increasingly rely on data-driven systems to streamline operations and deliver better services.""",

            """The author does well job on explaining the windows Modes. It would have been better if the author had included a snapshot of the single window enable/disable settings. I don’t think the author make any assumption because the document explains everything mentioned on the title page.""",

            """I think the tutorial is good overall. Some parts are easy to understand, but other parts could use more explanation. The images help, although a few of them are difficult to see. I would make some changes to improve the experience for beginners.""",

            """The tutorial explains how people can use the application. I liked some of the examples, but I also think a few sections could be shorter. The author should probably add more pictures because they would make the instructions easier to follow.""",

            """Technology has changed how people communicate with each other. Many people use social media to share information, pictures, and videos. I think these applications are useful, but people should also consider their privacy and how much information they share online.""",

            """The author explains the topic clearly in most sections. However, I noticed that some sentences are repetitive and some explanations are longer than necessary. Overall, the tutorial provides useful information for someone who is learning the application."""
        ],
    },

    {
        "name": "appeal path",
        "criterion": 4,
        # Submit this text first, then manually appeal using its returned content_id.
        # Also test an appeal with a nonexistent content_id and verify HTTP 404.
        "texts": [
            """Technology allows people to communicate and share information quickly. Online services make many everyday activities easier, but users should have a way to report problems and request a review when something goes wrong."""
        ],
    },

    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_missing_text"},
            {"text": "", "creator_id": "eval_empty_text"},
            {"text": "   ", "creator_id": "eval_whitespace_text"},
            {"text": "x" * 10001, "creator_id": "eval_oversized_text"},
        ],
    },
]
def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems

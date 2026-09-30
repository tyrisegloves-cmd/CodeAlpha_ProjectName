import random
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Post, Follow, Comment
User = get_user_model()

PEOPLE = [
 ("maya.okafor", "Maya", "Okafor", "Product designer at Lumen. Coffee, type and long walks.", "Accra, Ghana", [
   "Spent the morning deleting features from a prototype. User testing got noticeably happier. Less really is more.",
   "Hot take: a good empty state is the most underrated piece of UX.",
   "Reading 'The Design of Everyday Things' again. Still finding new things after the third time."]),
 ("daniel.reyes", "Daniel", "Reyes", "Backend engineer. Postgres fan. I write about boring, reliable systems.", "Austin, TX", [
   "Query went from 4s to 40ms with one composite index. Always read the query plan before adding a cache.",
   "Friendly reminder: backups you have never restored are just hopes.",
   "Code review tip: praise in public, nitpick in private."]),
 ("amara.nwosu", "Amara", "Nwosu", "Data scientist. Turning messy CSVs into clear stories.", "Lagos, Nigeria", [
   "Cleaned a dataset with 14 different spellings of 'Lagos'. Data work is 80% janitorial, 20% joy.",
   "Plot twist: the model was fine, the labels were wrong.",
   "Just gave my first conference talk. My hands shook for 5 minutes, then it was great!"]),
 ("kofi.mensah", "Kofi", "Mensah", "Founder building simple invoicing tools for small shops.", "Accra, Ghana", [
   "Shipped invoice reminders today. First customer said it saved her two hours a week. That is why we build.",
   "Lesson from month six: talk to ten customers before writing a single line of code.",
   "Hiring our first support person next month. Excited and nervous in equal measure."]),
 ("sofia.lindqvist", "Sofia", "Lindqvist", "Photographer and slow traveller. Chasing good light.", "Stockholm, Sweden", [
   "Golden hour over the archipelago tonight. Sometimes you just put the camera down and watch.",
   "Packing tip for photographers: one prime lens, one good book, nothing else.",
   "Finished editing the autumn series. Posting highlights this week."]),
 ("priya.raman", "Priya", "Raman", "Frontend developer. Accessibility is not optional.", "Bengaluru, India", [
   "Tried navigating our app with only a keyboard today. Found seven problems in ten minutes. Fixing them all this sprint.",
   "Contrast ratio is not a suggestion. Please check your greys.",
   "CSS grid still makes me smile every time a layout just works."]),
 ("tom.whitaker", "Tom", "Whitaker", "Marathon runner, occasional baker, full-time dad.", "Manchester, UK", [
   "20 miler done in the rain. Legs are jelly, sourdough is proofing, life is good.",
   "Race week. Trust the training, sleep early, and do not try anything new at breakfast.",
   "Third attempt at focaccia. The crumb is finally right!"]),
 ("lena.fischer", "Lena", "Fischer", "Climate researcher. Optimistic about what we can fix.", "Berlin, Germany", [
   "New paper out: cities that plant street trees cool down up to 3 degrees in summer. Cheap and effective.",
   "Cycled to work in the first frost. Berlin in autumn is unbeatable.",
   "Good news day: solar capacity installed this year beat every forecast."]),
]
COMMENTS = ["Love this.", "Couldn't agree more.", "This is so true!", "Congrats, well deserved!", "Needed to hear this today.",
            "Great tip, thanks for sharing.", "Would love to hear more about this.", "Same experience here.", "Brilliant."]

class Command(BaseCommand):
    help = "Create realistic demo data (all passwords: demo12345)"
    def handle(self, *a, **k):
        random.seed(7)
        User.objects.filter(username__in=["ada", "linus", "grace"]).delete()
        now, users, posts = timezone.now(), [], []
        for un, fn, ln, bio, loc, texts in PEOPLE:
            u, new = User.objects.get_or_create(username=un, defaults=dict(first_name=fn, last_name=ln))
            if new:
                u.set_password("demo12345"); u.save()
                u.profile.bio, u.profile.location = bio, loc; u.profile.save()
                for t in texts:
                    p = Post.objects.create(author=u, text=t)
                    Post.objects.filter(pk=p.pk).update(created=now - timedelta(minutes=random.randint(5, 4000)))
                    posts.append(p)
            users.append(u)
        if posts:
            for u in users:
                for o in random.sample([x for x in users if x != u], random.randint(3, 5)):
                    Follow.objects.get_or_create(follower=u, following=o)
            for p in posts:
                for l in random.sample([x for x in users if x != p.author], random.randint(0, 6)): p.likes.add(l)
                for c in random.sample([x for x in users if x != p.author], random.randint(0, 2)):
                    cm = Comment.objects.create(post=p, author=c, text=random.choice(COMMENTS))
                    Comment.objects.filter(pk=cm.pk).update(created=p.created + timedelta(minutes=random.randint(3, 300)))
        self.stdout.write("Done. Log in as maya.okafor / demo12345 (or any user listed in the README).")

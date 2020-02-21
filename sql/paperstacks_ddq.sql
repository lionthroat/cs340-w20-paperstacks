/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

drop table if exists Authors;
create table Authors (
  `author_id` int(11) not null auto_increment primary key,
  `author_name` varchar(255) COLLATE utf8_unicode_ci not null,
  `author_description` text COLLATE utf8_unicode_ci
) engine=innodb default charset=latin1;

drop table if exists Books;
create table Books (
  `isbn` int(11) not null primary key unique,
  `book_title` varchar(255) COLLATE utf8_unicode_ci not null,
  `year_published` int(11) not null,
  `book_description` text COLLATE utf8_unicode_ci,
  foreign key (`author_id`) references Authors (`author_id`)
) engine=innodb default charset=latin1;

drop table if exists Books_Authors;
create table Books_Authors (
  `isbn` int(11) not null,
  `author_id` int(11) not null,
  foreign key (`isbn`) references Books (`isbn`),
  foreign key (`author_id`) references Authors (`author_id`),
  primary key (`isbn`, `author_id`)
) engine=innodb default charset=latin1;

drop table if exists Genres;
create table Genres (
  `genre_id` int(11) not null auto_increment,
  `genre_name` varchar(255) COLLATE utf8_unicode_ci not null,
  KEY `genre_id` (`genre_id`)
) engine=innodb default charset=latin1;

drop table if exists Genres_Books;
create table Genres_Books (
  `genre_id` int(11) not null,
  `isbn` int(11) not null,
  KEY `FK_Genres_Books_Genres` (`genre_id`),
  KEY `FK_Genres_Books_Books` (`isbn`),
  CONSTRAINT `FK_Genres_Books_Books` FOREIGN KEY (`isbn`) REFERENCES `Books` (`isbn`),
  CONSTRAINT `FK_Genres_Books_Genres` FOREIGN KEY (`genre_id`) REFERENCES `Genres` (`genre_id`)
) engine=innodb default charset=latin1;

drop table if exists Ratings;
create table Ratings (
  `rating_id` int(11) primary key not null auto_increment,
  `review_id` int(11),
  `isbn` int(11) not null,
  `star_rating` int(11) not null,
  `rating_date` date not null,
  foreign key (`isbn`) references Books (`isbn`)
) engine=innodb default charset=latin1;

drop table if exists Reviews;
create table Reviews (
  `review_id` int(11) primary key not null auto_increment,
  `rating_id` int(11),
  `isbn` int(11) not null,
  `review_content` text COLLATE utf8_unicode_ci not null,
  `review_date` date not null,
  foreign key (`rating_id`) references Ratings (`rating_id`),
  foreign key (`isbn`) references Books (`isbn`)
) engine=innodb default charset=latin1;

alter table Ratings
add foreign key (`review_id`) references Reviews (`review_id`);

INSERT INTO `Genres` VALUES
  (1,'Art'),
  (2, 'Biography'),
  (3, 'Business'),
  (4, 'Children\'s Books'),
  (5, 'Classics'),
  (6, 'Cookbooks'),
  (7, 'Fantasty'),
  (8, 'Fiction'),
  (9, 'Historical Fiction'),
  (10, 'History'),
  (11, 'Memoir'),
  (12, 'Music'),
  (12, 'Mystery & Thriller'),
  (13, 'Nonfiction'),
  (14, 'Poetry'),
  (15, 'Romance'),
  (16, 'Science'),
  (17, 'Science Fiction'),
  (18, 'Self Help'),
  (19, 'Travel'),
  (20, 'Young Adult');

insert into `Authors` (author_id, author_name, author_description) values
  (100, 'Barbara Demick', 'Barbara Demick is Beijing bureau chief for the Los Angeles Times and author of Nothing to Envy: Ordinary Lives in North Korea. The book won the U.K.\'s top non-fiction prize, the Samuel Johnson award, in 2010 and was a finalist for both the National Book Awards and a National Book Critics Circle Awards. Demick\'s earlier book, Logavina Street: Life and Death in a Sarajevo Neighborhood is to be republished in 2012 by Granta.'),
  (101, 'Drew Daywalt', NULL),
  (102, 'Mary Robinette Kowal', 'Mary Robinette Kowal is the author of the Lady Astronaut duology and historical fantasy novels: The Glamourist Histories series and Ghost Talkers. She\'s a member of the award-winning podcast Writing Excuses and has received the Campbell Award for Best New Writer, three Hugo awards, the RT Reviews award for Best Fantasy Novel, and has been a finalist for the Hugo, Nebula, and Locus awards. Stories have appeared in Strange Horizons, Asimov\'s, several Year\'s Best anthologies and her collections Word Puppets and Scenting the Dark and Other Stories. As a professional puppeteer and voice actor (SAG/AFTRA), Mary has performed for LazyTown (CBS), the Center for Puppetry Arts, Jim Henson Pictures, and founded Other Hand Productions. Her designs have garnered two UNIMA-USA Citations of Excellence, the highest award an American puppeteer can achieve. She records fiction for authors such as Kage Baker, Cory Doctorow and John Scalzi. Mary lives in Chicago with her husband Rob and over a dozen manual typewriters.'),
  (103, 'Samin Nosrat', 'SAMIN NOSRAT is a chef, teacher, and author of the best-selling, James Beard award-winning Salt, Fat, Acid, Heat. She has been called "a go to resource for matching the correct techniques with the best ingredients" by The New York Times and "the next Julia Child" by NPR\'s "All Things Considered." Samin is an EAT columnist for The New York Times Magazine and can be found eating, cooking, and laughing in the "Salt, Fat, Acid, Heat" documentary series on Netflix.'),
  (104, 'David W. Blight', 'David W. Blight is the Sterling Professor of History and Director of the Gilder Lehrman Center for the Study of Slavery, Resistance, and Abolition at Yale University. He is the author or editor of a dozen books, including American Oracle: The Civil War in the Civil Rights Era; and Race and Reunion: The Civil War in American Memory; and annotated editions of Douglass’s first two autobiographies. He has worked on Douglass much of his professional life, and been awarded the Bancroft Prize, the Abraham Lincoln Prize, and the Frederick Douglass Prize, among others.'),
  (105, 'Gillian Flynn', 'Gillian Flynn is the author of the #1 New York Times bestseller Gone Girl, for which she wrote the Golden Globe-nominated screenplay, and the New York Times bestsellers Dark Places and Sharp Objects. A former critic for Entertainment Weekly, she lives in Chicago with her husband and children.'),
  (106, 'Gayle Laakmann McDowell', 'Gayle Laakmann McDowell is the founder and CEO of CareerCup and the author of Cracking the PM Interview and Cracking the Tech Career. Her background is in software development. She has worked as a software engineer at Google, Microsoft, and Apple. At Google, she interviewed hundreds of software engineers and evaluated thousands of hiring packets on the hiring committee. She holds a B.S.E. and M.S.E. in computer science from the University of Pennsylvania and an MBA from the Wharton School. She now consults with tech companies to improve their hiring process and with startups to prepare them for acquisition interviews.'),
  (107, 'Eve L. Ewing', 'Electric Arches is an imaginative exploration of Black girlhood and womanhood through poetry, visual art, and narrative prose. Blending stark realism with the surreal and fantastic, Eve L. Ewing’s narrative takes us from the streets of 1990s Chicago to an unspecified future, deftly navigating the boundaries of space, time, and reality. Ewing imagines familiar figures in magical circumstances―blues legend Koko Taylor is a tall-tale hero; LeBron James travels through time and encounters his teenage self. She identifies everyday objects―hair moisturizer, a spiral notebook―as precious icons. Her visual art is spare, playful, and poignant―a cereal box decoder ring that allows the wearer to understand what Black girls are saying; a teacher’s angry, subversive message scrawled on the chalkboard. Electric Arches invites fresh conversations about race, gender, the city, identity, and the joy and pain of growing up.'),
  (108, 'Mary Shelley', 'Mary Shelley (1797-1851), the only daughter of writers William Godwin and Mary Wollstonecraft, and wife of Percy Bysshe Shelley, is the critically acclaimed author of Frankenstein, Valperga, and The Last Man, in addition to many other works. Mary Shelley s writings reflect and were influenced by a number of literary traditions including Gothic and Romantic ideals, and Frankenstein is widely regarded as the first modern work of science fiction. Today s scholarship of Mary Shelley s writings reveal her to be a political radical, as demonstrated though recurring themes of cooperation and sympathy, particularly among women, in her work, which are in direct conflict with the individual Romantic ideals of the eighteenth and nineteenth centuries.'),
  (109, 'Jane Austen', 'One of England\'s most beloved authors, Jane Austen wrote such classic novels as Pride and Prejudice, Sense and Sensibility, Emma, and Northanger Abbey. Published anonymously during her life, Austen\'s work was renowned for its realism, humour, and commentary on English social rites and society at the time. Austen\'s writing was supported by her family, particularly by her brother, Henry, and sister, Cassandra, who is believed to have destroyed, at Austen\'s request, her personal correspondence after Austen\'s death in 1817. Austen\'s authorship was revealed by her nephew in A Memoir of Jane Austen, published in 1869, and the literary value of her work has since been recognized by scholars around the world.'),
  (110, 'Del Sroufe', 'Del Sroufe has worked as chef and co-owner at Wellness Forum Foods for six years, a plant-based meal delivery and catering service that emphasizes healthy, minimally processed foods, produces a line of "in the bag mixes," and offers cooking classes to the public. He has worked in vegan and vegetarian kitchens for 22 years, including spending time as a vegan personal chef. He lives, works, and cooks in Columbus, OH.'),
  (111, 'Madeline Puckette', 'Madeline Puckette is a sommelier and visual designer whose electrifying infographics and congenial writing has garnered an enthusiastic following from wine beginner to wine expert. Her work has been applied in organizations, including The Court of Master Sommeliers and the Guild of Sommeliers to help wine professionals learn.'),
  (112, 'Evi Nemeth', 'Evi Nemeth pioneered the discipline of UNIX system administration. She taught and mentored computer science students at the University of Colorado Boulder, was visiting faculty member at Dartmouth College and UC San Diego, and helped bring Internet technology to the developing world through her work with the Internet Society and the United Nations.'),
  (113, 'Julia Evans', 'Julia Evans is a Montreal-based software developer at Stripe. She\'s a co-organizer of !!con, a regular speaker at programming conferences, and an author of awesome programming zines.'),
  (114, 'Barbara Oakley PhD', 'Barbara Oakley is a professor of engineering at Oakland University in Rochester, Michigan. Her research has been termed "revolutionary" by the Wall Street Journal. She has received many national awards for her teaching, including the American Society of Engineering Education Chester F. Carlson Award for outstanding technical innovation in STEM pedagogy and the Theo L. Pilkington Award for exemplary work in bioengineering education. Her Coursera-UC San Diego course Learning How to Learn, created with her co-instructor Terrence Sejnowski, the Francis Crick Professor at the Salk Institute, is the most popular massive open online course in the world, with nearly 2 million students to date.'),
  (115, 'Toni Morrison', 'Toni Morrison was awarded the Nobel Prize for Literature in 1993. She is the author of several novels, including The Bluest Eye, Beloved (made into a major film), and Love. She has received the National Book Critics Circle Award and a Pulitzer Prize. She was the Robert F. Goheen Professor at Princeton University.'),
  (116, 'Delia Owens', NULL),
  (117, 'Maryanne Wolf', 'Maryanne Wolf, the John DiBiaggio Professor of Citizenship and Public Service at Tufts University, was the director of the Tufts Center for Reading and Language Research. She currently directs the Center for Dyslexia, Diverse Learners, and Social Justice at UCLA, and is working with the Dyslexia Center at the UCSF School of Medicine and with Curious Learning: A Global Literacy Project, which she co-founded. She is the recipient of multiple research and teaching honors, including the highest awards by the International Dyslexia Association and the Australian Learning Disabilities Association. She is the author of Proust and the Squid (HarperCollins), Tales of Literacy for the 21st Century (Oxford University Press), and more than 160 scientific publications.'),
  (118, 'Rupi Kaur', 'Rupi Kaur is a poet, artist, and performer. Her works have taken the literary world by storm. Her second book, the sun and her flowers—an instant global bestseller, is an artistic sibling to her debut, milk and honey—one of America\'s bestselling books of 2017. “i am the product of all the ancestors getting together and deciding these stories need to be told.” Rupi sees her work as an articulation of this vision. She’s an eternal artist. At the age of five, her mother handed her a paintbrush and said, “draw your heart out.” At seventeen, she happened upon a local open mic night where she performed her first spoken word poem. She fell in love with performance poetry that night. Rupi continued performing across Canada, while building a community of readers and poetry enthusiasts. While studying at the University of Waterloo, Rupi wrote, illustrated, and self-published her first collection, milk and honey. In the years since, milk and honey has become an international phenomenon. It’s sold over 3 million copies, been translated into more than 35 languages, and landed as a #1 New York Times bestseller—where it has spent more than 100 consecutive weeks.'),
  (119, 'Olivia Koski', 'Olivia Koski was born in the desert and raised in the mountains. She is head of operations for Guerilla Science, an organization that connects the public with science in novel ways. Previously she worked as a senior producer at The Atavist Magazine and a laser engineer at Lockheed Martin. She has a master\'s in journalism from New York University and bachelor\'s degrees in engineering physics and Germanic studies from the University of Colorado.'),
  (120, 'Nnedi Okorafor', 'Nnedi Okorafor\’s books include Lagoon (a British Science Fiction Association Award finalist for Best Novel), Who Fears Death (a World Fantasy Award winner for Best Novel), Kabu Kabu (a Publisher\'s Weekly Best Book for Fall 2013), Akata Witch (an Amazon.com Best Book of the Year), Zahrah the Windseeker (winner of the Wole Soyinka Prize for African Literature), and The Shadow Speaker (a CBS Parallax Award winner).'),
  (121, 'Mary Roach', 'Mary Roach is the author of Grunt: The Curious Science of Humans at War, Packing for Mars: The Curious Science of Life in the Void, Bonk: The Curious Coupling of Science and Sex, Spook: Science Tackles the Afterlife, and Stiff: The Curious Lives of Human Cadavers. Her writing has appeared in Outside, Wired, National Geographic, and the New York Times Magazine, among others. She lives in Oakland, California.');

insert into `Books` (isbn, book_title, year_published, genre_id, book_description) values
  (0385523912, 'Nothing to Envy: Ordinary Lives in North Korea', 2013, 'Demick brings to life what it means to be living under the most repressive regime today—an Orwellian world that is by choice not connected to the Internet, where displays of affection are punished, informants are rewarded, and an offhand remark can send a person to the gulag for life. She takes us deep inside the country, beyond the reach of government censors, and through meticulous and sensitive reporting we see her subjects fall in love, raise families, nurture ambitions, and struggle for survival. One by one, we witness their profound, life-altering disillusionment with the government and their realization that, rather than providing them with lives of abundance, their country has betrayed them.'),
  (0399255370, 'The Day the Crayons Quit', 2013, 'Poor Duncan just wants to color. But when he opens his box of crayons, he finds only letters, all saying the same thing: His crayons have had enough! They quit! Beige Crayon is tired of playing second fiddle to Brown Crayon. Black wants to be used for more than just outlining. Blue needs a break from coloring all those bodies of water. And Orange and Yellow are no longer speaking—each believes he is the true color of the sun.'),
  (0765378388, 'The Calculating Stars: A Lady Astronaut Novel', 2018, 'On a cold spring night in 1952, a huge meteorite fell to earth and obliterated much of the east coast of the United States, including Washington D.C. The ensuing climate cataclysm will soon render the earth inhospitable for humanity, as the last such meteorite did for the dinosaurs. This looming threat calls for a radically accelerated effort to colonize space, and requires a much larger share of humanity to take part in the process.'),
  (1476753830, 'Salt, Fat, Acid, Heat: Mastering the Elements of Good Cooking', 2017, 'In the tradition of The Joy of Cooking and How to Cook Everything comes Salt, Fat, Acid, Heat, an ambitious new approach to cooking by a major new culinary voice. Chef and writer Samin Nosrat has taught everyone from professional chefs to middle school kids to author Michael Pollan to cook using her revolutionary, yet simple, philosophy. Master the use of just four elements—Salt, which enhances flavor; Fat, which delivers flavor and generates texture; Acid, which balances flavor; and Heat, which ultimately determines the texture of food—and anything you cook will be delicious. By explaining the hows and whys of good cooking, Salt, Fat, Acid, Heat will teach and inspire a new generation of cooks how to confidently make better decisions in the kitchen and cook delicious meals with any ingredients, anywhere, at any time.'),
  (1416590323, 'Frederick Douglass: Prophet of Freedom', 2020, 'As a young man Frederick Douglass (1818–1895) escaped from slavery in Baltimore, Maryland. He was fortunate to have been taught to read by his slave owner mistress, and he would go on to become one of the major literary figures of his time. His very existence gave the lie to slave owners: with dignity and great intelligence he bore witness to the brutality of slavery. Initially mentored by William Lloyd Garrison, Douglass spoke widely, using his own story to condemn slavery. By the Civil War, Douglass had become the most famed and widely travelled orator in the nation. In his unique and eloquent voice, written and spoken, Douglass was a fierce critic of the United States as well as a radical patriot. After the war he sometimes argued politically with younger African Americans, but he never forsook either the Republican party or the cause of black civil and political rights. In this “cinematic and deeply engaging” (The New York Times Book Review) biography, David Blight has drawn on new information held in a private collection that few other historian have consulted, as well as recently discovered issues of Douglass’s newspapers. “Absorbing and even moving…a brilliant book that speaks to our own time as well as Douglass’s” (The Wall Street Journal), Blight’s biography tells the fascinating story of Douglass’s two marriages and his complex extended family. “David Blight has written the definitive biography of Frederick Douglass…a powerful portrait of one of the most important American voices of the nineteenth century” (The Boston Globe).'),
  (0297859382, 'Gone Girl', 2012, 'On a warm summer morning in North Carthage, Missouri, it is Nick and Amy Dunne’s fifth wedding anniversary. Presents are being wrapped and reservations are being made when Nick’s clever and beautiful wife disappears. Nick is oddly evasive, and he’s definitely bitter—but is he really a killer?'),
  (0984782850, 'Cracking the Coding Interview: 189 Programming Questions and Solutions', 2015, 'I am not a recruiter. I am a software engineer. And as such, I know what it\'s like to be asked to whip up brilliant algorithms on the spot and then write flawless code on a whiteboard. I\'ve been through this as a candidate and as an interviewer. Cracking the Coding Interview, 6th Edition is here to help you through this process, teaching you what you need to know and enabling you to perform at your very best. I\'ve coached and interviewed hundreds of software engineers. The result is this book. Learn how to uncover the hints and hidden details in a question, discover how to break down a problem into manageable chunks, develop techniques to unstick yourself when stuck, learn (or re-learn) core computer science concepts, and practice on 189 interview questions and solutions. These interview questions are real; they are not pulled out of computer science textbooks. They reflect what\'s truly being asked at the top companies, so that you can be as prepared as possible.'),
  (1608468569, 'Electric Arches', 2017, 'Electric Arches is an imaginative exploration of Black girlhood and womanhood through poetry, visual art, and narrative prose. Blending stark realism with the surreal and fantastic, Eve L. Ewing’s narrative takes us from the streets of 1990s Chicago to an unspecified future, deftly navigating the boundaries of space, time, and reality. Ewing imagines familiar figures in magical circumstances―blues legend Koko Taylor is a tall-tale hero; LeBron James travels through time and encounters his teenage self. She identifies everyday objects―hair moisturizer, a spiral notebook―as precious icons. Her visual art is spare, playful, and poignant―a cereal box decoder ring that allows the wearer to understand what Black girls are saying; a teacher’s angry, subversive message scrawled on the chalkboard. Electric Arches invites fresh conversations about race, gender, the city, identity, and the joy and pain of growing up.'),
  (1512308056, 'Frankenstein', 1818, 'Frankenstein; or, The Modern Prometheus, is a novel written by English author Mary Shelley about the young student of science Victor Frankenstein, who creates a grotesque but sentient creature in an unorthodox scientific experiment. Shelley started writing the story when she was eighteen, and the novel was published when she was twenty. The first edition was published anonymously in London in 1818. Shelley\'s name appears on the second edition, published in France in 1823. Shelley had travelled through Europe in 1814, journeying along the river Rhine in Germany with a stop in Gernsheim which is just 17 km (10 mi) away from Frankenstein Castle, where two centuries before an alchemist was engaged in experiments. Later, she travelled in the region of Geneva (Switzerland)—where much of the story takes place—and the topics of galvanism and other similar occult ideas were themes of conversation among her companions, particularly her lover and future husband, Percy Shelley. Mary, Percy, Lord Byron, and John Polidori decided to have a competition to see who could write the best horror story. After thinking for days, Shelley dreamt about a scientist who created life and was horrified by what he had made; her dream later evolved into the story within the novel.'),
  (0141439518, 'Pride and Prejudice', 1813, 'Pride and Prejudice is a novel of manners by Jane Austen, first published in 1813. The story follows the main character, Elizabeth Bennet, as she deals with issues of manners, upbringing, morality, education, and marriage in the society of the landed gentry of the British Regency. Elizabeth is the second of five daughters of a country gentleman living near the fictional town of Meryton in Hertfordshire, near London.Page 2 of a letter from Jane Austen to her sister Cassandra (11 June 1799) in which she first mentions Pride and Prejudice, using its working title First Impressions.Set in England in the early 19th century, Pride and Prejudice tells the story of Mr and Mrs Bennet\'s five unmarried daughters after the rich and eligible Mr Bingley and his status-conscious friend, Mr Darcy, have moved into their neighbourhood.'),
  (1615190614, 'Forks Over Knives―The Cookbook: Over 300 Recipes for Plant-Based Eating All Through the Year', 2012, 'Forks Over Knives—the book, the film, the movement—is back again in a cookbook. The secret is out: If you want to lose weight, lower your cholesterol, avoid cancer, and prevent (or even reverse) type 2 diabetes and heart disease, the right food is your best medicine. Thousands of people have cut out meat, dairy, and oils and seen amazing results. If you’re among them—or you’d like to be—you need this cookbook.
  Del Sroufe, the man behind some of the mouthwatering meals in the landmark documentary, proves that the Forks Over Knives philosophy is not about what you can’t eat, but what you can. Chef Del and his collaborators Julieanna Hever, Judy Micklewright, Darshana Thacker, and Isa Chandra Moskowitz transform wholesome fruits, vegetables, grains, and legumes into hundreds of recipes—classic and unexpected, globally and seasonally inspired, and for every meal of the day, all through the year.'),
  (1592408990, 'Wine Folly: The Essential Guide to Wine', 2015, 'Red or white? Cabernet or merlot? Light or bold? What to pair with food? Drinking great wine isn’t hard, but finding great wine does require a deeper understanding of the fundamentals. Wine Folly: The Essential Guide to Wine will help you make sense of it all in a unique infographic wine book. Designed by the creators of WineFolly.com, which has won Wine Blogger of the Year from the International Wine & Spirits Competition, this book combines sleek, modern information design with data visualization and gives readers pragmatic answers to all their wine questions'),
  (0134277554, 'UNIX and Linux System Administration Handbook (5th Edition)', 2017, 'UNIX® and Linux® System Administration Handbook, Fifth Edition, is today’s definitive guide to installing, configuring, and maintaining any UNIX or Linux system, including systems that supply core Internet and cloud infrastructure. Updated for new distributions and cloud environments, this comprehensive guide covers best practices for every facet of system administration, including storage management, network design and administration, security, web hosting, automation, configuration management, performance analysis, virtualization, DNS, security, and the management of IT service organizations. The authors—world-class, hands-on technologists—offer indispensable new coverage of cloud platforms, the DevOps philosophy, continuous deployment, containerization, monitoring, and many other essential topics.'),
  (1593279779, 'Your Linux Toolbox', 2019, 'Get the most out of your Linux system using tools you already have! These illustrated zines by Julia Evans (@b0rk) will teach you how simple it can be to tame the powerful beast called Linux. And for the first time, her tips and tricks are together in one place. Find out what your programs are doing and why. Understand how your system\'s parts talk to each other and what to do when they bicker. And see how a cat GIF travels from a distant server to your very own screen.'),
  (0399165245, 'A Mind for Numbers: How to Excel at Math and Science (Even If You Flunked Algebra)', 2014, 'Whether you are a student struggling to fulfill a math or science requirement, or you are embarking on a career change that requires a new skill set, A Mind for Numbers offers the tools you need to get a better grasp of that intimidating material. Engineering professor Barbara Oakley knows firsthand how it feels to struggle with math. She flunked her way through high school math and science courses, before enlisting in the army immediately after graduation. When she saw how her lack of mathematical and technical savvy severely limited her options—both to rise in the military and to explore other careers—she returned to school with a newfound determination to re-tool her brain to master the very subjects that had given her so much trouble throughout her entire life.'),
  (1400033411, 'Beloved', 2004, 'Staring unflinchingly into the abyss of slavery, this spellbinding novel transforms history into a story as powerful as Exodus and as intimate as a lullaby. Sethe, its protagonist, was born a slave and escaped to Ohio, but eighteen years later she is still not free. She has too many memories of Sweet Home, the beautiful farm where so many hideous things happened. And Sethe’s new home is haunted by the ghost of her baby, who died nameless and whose tombstone is engraved with a single word: Beloved. Filled with bitter poetry and suspense as taut as a rope, Beloved is a towering achievement.'),
  (1984827618, 'Where the Crawdads Sing', 2018, 'For years, rumors of the "Marsh Girl" have haunted Barkley Cove, a quiet town on the North Carolina coast. So in late 1969, when handsome Chase Andrews is found dead, the locals immediately suspect Kya Clark, the so-called Marsh Girl. But Kya is not what they say. Sensitive and intelligent, she has survived for years alone in the marsh that she calls home, finding friends in the gulls and lessons in the sand. Then the time comes when she yearns to be touched and loved. When two young men from town become intrigued by her wild beauty, Kya opens herself to a new life--until the unthinkable happens. Where the Crawdads Sing is at once an exquisite ode to the natural world, a heartbreaking coming-of-age story, and a surprising tale of possible murder. Owens reminds us that we are forever shaped by the children we once were, and that we are all subject to the beautiful and violent secrets that nature keeps.'),
  (0060933845, 'Proust and the Squid: The Story and Science of the Reading Brain', 2008, '"Human beings were never born to read," writes Tufts University cognitive neuroscientist and child development expert Maryanne Wolf. Reading is a human invention that reflects how the brain rearranges itself to learn something new. In this ambitious, provocative book, Wolf chronicles the remarkable journey of the reading brain not only over the past five thousand years, since writing began, but also over the course of a single child\'s life, showing in the process why children with dyslexia have reading difficulties and singular gifts. Lively, erudite, and rich with examples, Proust and the Squid asserts that the brain that examined the tiny clay tablets of the Sumerians was a very different brain from the one that is immersed in today\'s technology-driven literacy. The potential transformations in this changed reading brain, Wolf argues, have profound implications for every child and for the intellectual development of our species.'),
  (1449474256, 'Milk and Honey', 2015, '#1 New York Times bestseller Milk and Honey is a collection of poetry and prose about survival. About the experience of violence, abuse, love, loss, and femininity. The book is divided into four chapters, and each chapter serves a different purpose. Deals with a different pain. Heals a different heartache. Milk and Honey takes readers through a journey of the most bitter moments in life and finds sweetness in them because there is sweetness everywhere if you are just willing to look.'),
  (0143129775, 'Vacation Guide to the Solar System: Science for the Savvy Space Traveler!', 2017, 'Packed with real science and fueled by imagination, a beautifully illustrated travel guide to traveling in our solar system. Imagine taking a hike along the windswept red plains of Mars to dig for signs of life, or touring one of Jupiter\'s sixty-four moons where you can photograph its swirling storms. For a shorter trip on a tight budget, the Moon is quite majestic and very quiet if you can make it during the off-season.With four-color illustrations and packed with real-world science, The Vacation Guide to the Solar System is the must-have planning guide for the curious space adventurer, covering all of the essentials for your next voyage, how to get there, and what to do when you arrive. Written by an astronomer who presents at the Hayden Planetarium and one of the creators of the Guerilla Science collective, this tongue-in-cheek reference guide is an imaginative exploration into the "What if" of space travel, sharing fascinating facts about space, the planets in our solar system, and even some moons!'),
  (1250203422, 'Binti', 2018, 'Her name is Binti, and she is the first of the Himba people ever to be offered a place at Oomza University, the finest institution of higher learning in the galaxy. But to accept the offer will mean giving up her place in her family to travel between the stars among strangers who do not share her ways or respect her customs.'),
  (0393354377, 'Grunt: The Curious Science of Humans at War', 2017, 'Grunt tackles the science behind some of a soldier\'s most challenging adversaries―panic, exhaustion, heat, noise―and introduces us to the scientists who seek to conquer them.'),
  (0393068471, 'Packing for Mars: The Curious Science of Life in the Void', 2010, 'In Packing for Mars, Roach tackles the strange science of space travel, and the psychology, technology, and politics that go into sending a crew into orbit.'),
  (0393329127, 'Spook: Science Tackles the Afterlife', 2006, '"What happens when we die? Does the light just go out and that\'s that―the million-year nap? Or will some part of my personality, my me-ness persist? What will that feel like? What will I do all day? Is there a place to plug in my lap-top?" In an attempt to find out, Mary Roach brings her tireless curiosity to bear on an array of contemporary and historical soul-searchers: scientists, schemers, engineers, mediums, all trying to prove (or disprove) that life goes on after we die.'),
  (0393324826, 'Stiff: The Curious Lives of Human Cadavers', 2004, 'Stiff is an oddly compelling, often hilarious exploration of the strange lives of our bodies postmortem. For two thousand years, cadavers―some willingly, some unwittingly―have been involved in science\'s boldest strides and weirdest undertakings. In this fascinating account, Mary Roach visits the good deeds of cadavers over the centuries and tells the engrossing story of our bodies when we are no longer with them.');

insert into `Books_Authors` (isbn, author_id) values
  (0385523912, 100),
  (0765378388, 102),
  (1476753830, 103),
  (1416590323, 104),
  (0297859382, 105),
  (0984782850, 106),
  (1608468569, 107),
  (1512308056, 108),
  (0141439518, 109),
  (1615190614, 110),
  (1592408990, 111),
  (0134277554, 112),
  (1593279779, 113),
  (0399165245, 114),
  (1400033411, 115),
  (1984827618, 116),
  (0060933845, 117),
  (1449474256, 118),
  (0143129775, 119),
  (1250203422, 120),
  (0393354377, 121),
  (0393068471, 121),
  (0393329127, 121),
  (0393324826, 121);

insert into `Genres_Books` (isbn, genre_id) values
  (0385523912, 13),
  (0765378388, 1),
  (1476753830, 18),
  (1416590323, 6),
  (0297859382, 2),
  (0984782850, 13),
  (1608468569, 3),
  (1512308056, 15),
  (0141439518, 5),
  (1615190614, 9),
  (1592408990, 6),
  (0134277554, 6),
  (1593279779, 3),
  (0399165245, 3),
  (1400033411, 13),
  (1984827618, 8),
  (0060933845, 8),
  (1449474256, 13),
  (0143129775, 14),
  (1250203422, 19),
  (0393354377, 13),
  (0393068471, 16),
  (0393329127, 16),
  (0393324826, 16);

insert into `Ratings` (rating_id, review_id, isbn, star_rating, rating_date) values
  (1000, NULL, 0399255370, 1, '2017-01-05'),
  (1001, NULL, 0399255370, 5, '2019-03-26'),
  (1002, NULL, 0399255370, 4, '2018-06-22'),
  (1003, NULL, 0984782850, 5, '2015-07-15'),
  (1004, NULL, 1592408990, 3, '2019-10-29'),
  (1005, NULL, 0765378388, 3, '2020-02-03'),
  (1006, NULL, 1512308056, 5, '2020-01-17'),
  (1007, NULL, 1449474256, 2, '2019-12-12'),
  (1008, NULL, 1476753830, 4, '2019-11-08');

insert into `Reviews` (review_id, rating_id, isbn, review_content, review_date) values
  (2000, 1000, 0399255370, 'What a terrible book! So many people hyped it up; gravely disappointing waste of money and time.', '2017-01-05'),
  (2001, 1001, 0399255370, 'Kid loves this book. Great additiong to the library', '2019-03-26'),
  (2002, NULL, 0399255370, 'Great book', '2018-06-22'),
  (2003, 1003, 0984782850, 'Helped get me a job at Amazon! Great book.', '2015-07-15'),
  (2004, 1004, 1592408990, 'Seems like more of a pretty coffee table book than anything, still an OK buy.', '2019-10-29'),
  (2005, NULL, 1984827618, 3, 'I can normally extend an author my suspension of disbelief to dive into their work of fiction, but in this case, the stretch was too great. Wonky plotlines sunk otherwise sumptuous prose.');

-- Link Reviews with their associated Ratings
update `Ratings` set review_id = 2000 where rating_id = 1000;
update `Ratings` set review_id = 2001 where rating_id = 1001;
update `Ratings` set review_id = 2003 where rating_id = 1003;
update `Ratings` set review_id = 2004 where rating_id = 1004;

select * from Authors;
select * from Books;
select * from Books_Authors;
select * from Genres;
select * from Genres_Books;
select * from Ratings;
select * from Reviews;

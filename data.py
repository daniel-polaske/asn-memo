"""Network data definitions for ASN Memo."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Tier(Enum):
    """Network tier classification."""
    TIER_1 = "Tier 1"
    TIER_2 = "Tier 2"
    TIER_3 = "Tier 3"
    CDN = "CDN"
    CLOUD = "Cloud Provider"
    IXP = "Internet Exchange"


@dataclass
class Network:
    """Represents a network with its AS number and metadata."""
    asn: int
    name: str
    tier: Tier
    headquarters: str = ""
    specialization: str = ""
    facts: List[str] = field(default_factory=list)


# Comprehensive network data
NETWORKS: List[Network] = [
    # === TIER 1 NETWORKS (Transit-Free Backbone Providers) ===
    Network(
        asn=3356,
        name="Lumen Technologies",
        tier=Tier.TIER_1,
        headquarters="Monroe, Louisiana, USA",
        specialization="Global backbone, formerly CenturyLink/Level 3",
        facts=[
            "Formed from CenturyLink's acquisition of Level 3 in 2017",
            "One of the largest global IP backbones",
            "Operates extensive fiber network across North America, Europe, and Asia",
        ],
    ),
    Network(
        asn=174,
        name="Cogent Communications",
        tier=Tier.TIER_1,
        headquarters="Washington, D.C., USA",
        specialization="Low-cost transit, aggressive peering policies",
        facts=[
            "Known for aggressive pricing and peering disputes",
            "Transit-free since 2004",
            "Focused on high-bandwidth business customers",
        ],
    ),
    Network(
        asn=2914,
        name="NTT Communications",
        tier=Tier.TIER_1,
        headquarters="Tokyo, Japan",
        specialization="Global Tier 1, strong Asia-Pacific presence",
        facts=[
            "Subsidiary of Nippon Telegraph and Telephone",
            "Operates Global IP Network (GIN)",
            "Major presence in Asia, Americas, and Europe",
        ],
    ),
    Network(
        asn=1299,
        name="Arelion (formerly Telia Carrier)",
        tier=Tier.TIER_1,
        headquarters="Stockholm, Sweden",
        specialization="European backbone, transatlantic cables",
        facts=[
            "Rebranded from Telia Carrier in 2022",
            "Owns extensive submarine cable systems",
            "Strong presence in Northern Europe and transatlantic routes",
        ],
    ),
    Network(
        asn=3257,
        name="GTT Communications",
        tier=Tier.TIER_1,
        headquarters="McLean, Virginia, USA",
        specialization="Enterprise networking, global backbone",
        facts=[
            "Grew through acquisitions (Interoute, Hibernia)",
            "Focus on multinational enterprise customers",
            "Operates Tier 1 IP backbone",
        ],
    ),
    Network(
        asn=6762,
        name="Telecom Italia Sparkle",
        tier=Tier.TIER_1,
        headquarters="Rome, Italy",
        specialization="Mediterranean connectivity, submarine cables",
        facts=[
            "International arm of Telecom Italia",
            "Strong presence in Mediterranean and Middle East",
            "Operates Seabone global backbone",
        ],
    ),
    Network(
        asn=6453,
        name="TATA Communications",
        tier=Tier.TIER_1,
        headquarters="Mumbai, India",
        specialization="India connectivity, submarine cables",
        facts=[
            "Owns the largest submarine cable network globally",
            "Strong presence in emerging markets",
            "Formerly VSNL (Videsh Sanchar Nigam Limited)",
        ],
    ),
    Network(
        asn=701,
        name="Verizon Business",
        tier=Tier.TIER_1,
        headquarters="Basking Ridge, New Jersey, USA",
        specialization="Enterprise services, US backbone",
        facts=[
            "One of the original Internet backbone providers",
            "Acquired MCI/UUNET in 2006",
            "Major enterprise and government contracts",
        ],
    ),
    Network(
        asn=7018,
        name="AT&T",
        tier=Tier.TIER_1,
        headquarters="Dallas, Texas, USA",
        specialization="US telecommunications, global backbone",
        facts=[
            "Largest telecommunications company in the world by revenue",
            "Extensive US fiber infrastructure",
            "Major mobile carrier and ISP",
        ],
    ),
    Network(
        asn=3491,
        name="PCCW Global",
        tier=Tier.TIER_1,
        headquarters="Hong Kong",
        specialization="Asia-Pacific connectivity",
        facts=[
            "Subsidiary of PCCW Limited",
            "Strong presence in Greater China and Asia-Pacific",
            "Operates extensive submarine cable systems in Asia",
        ],
    ),
    Network(
        asn=5511,
        name="Orange S.A.",
        tier=Tier.TIER_1,
        headquarters="Paris, France",
        specialization="European backbone, Africa presence",
        facts=[
            "Formerly France Telecom",
            "Major presence in Europe and Africa",
            "One of the largest European carriers",
        ],
    ),
    Network(
        asn=6830,
        name="Liberty Global",
        tier=Tier.TIER_1,
        headquarters="London, UK / Denver, USA",
        specialization="European cable networks",
        facts=[
            "Largest cable operator in Europe",
            "Owns Virgin Media, Telenet, UPC",
            "Strong residential broadband focus",
        ],
    ),
    Network(
        asn=1239,
        name="Sprint (T-Mobile)",
        tier=Tier.TIER_1,
        headquarters="Overland Park, Kansas, USA",
        specialization="US backbone, merged with T-Mobile",
        facts=[
            "Merged with T-Mobile in 2020",
            "Historic Tier 1 backbone provider",
            "SprintLink was major IP transit network",
        ],
    ),
    Network(
        asn=12956,
        name="Telefonica",
        tier=Tier.TIER_1,
        headquarters="Madrid, Spain",
        specialization="Spain and Latin America connectivity",
        facts=[
            "Major presence in Spanish-speaking countries",
            "Operates under Movistar brand",
            "Strong Latin American backbone",
        ],
    ),

    # === TIER 2 NETWORKS (Regional Carriers) ===
    Network(
        asn=6939,
        name="Hurricane Electric",
        tier=Tier.TIER_2,
        headquarters="Fremont, California, USA",
        specialization="IPv6 pioneer, extensive peering",
        facts=[
            "Largest IPv6 backbone in the world",
            "Free IPv6 tunnel broker service",
            "Peers at most major IXPs globally",
            "Known for aggressive peering policy",
        ],
    ),
    Network(
        asn=7922,
        name="Comcast",
        tier=Tier.TIER_2,
        headquarters="Philadelphia, Pennsylvania, USA",
        specialization="US cable ISP, Xfinity brand",
        facts=[
            "Largest cable company in the United States",
            "Operates under Xfinity brand for consumers",
            "Major residential broadband provider",
        ],
    ),
    Network(
        asn=4134,
        name="China Telecom",
        tier=Tier.TIER_2,
        headquarters="Beijing, China",
        specialization="Chinese backbone, ChinaNet",
        facts=[
            "One of the 'Big Three' Chinese carriers",
            "Operates ChinaNet backbone",
            "Largest fixed-line operator in China",
        ],
    ),
    Network(
        asn=4837,
        name="China Unicom",
        tier=Tier.TIER_2,
        headquarters="Beijing, China",
        specialization="Chinese backbone, CNCGROUP",
        facts=[
            "Second largest Chinese carrier",
            "Strong mobile presence in China",
            "Operates China169 backbone",
        ],
    ),
    Network(
        asn=9002,
        name="RETN",
        tier=Tier.TIER_2,
        headquarters="London, UK",
        specialization="Europe to Asia connectivity",
        facts=[
            "Connects Europe to Asia via Russia",
            "Low-latency routes between continents",
            "Independent pan-European carrier",
        ],
    ),
    Network(
        asn=3320,
        name="Deutsche Telekom",
        tier=Tier.TIER_2,
        headquarters="Bonn, Germany",
        specialization="German backbone, European presence",
        facts=[
            "Largest telecommunications provider in Europe",
            "Parent company of T-Mobile US",
            "Strong enterprise services division",
        ],
    ),
    Network(
        asn=2516,
        name="KDDI Corporation",
        tier=Tier.TIER_2,
        headquarters="Tokyo, Japan",
        specialization="Japanese carrier, Asia-Pacific",
        facts=[
            "Second largest Japanese carrier",
            "Operates au mobile brand",
            "Strong presence in Asia-Pacific submarine cables",
        ],
    ),
    Network(
        asn=4766,
        name="Korea Telecom",
        tier=Tier.TIER_2,
        headquarters="Seongnam, South Korea",
        specialization="South Korean backbone",
        facts=[
            "Largest telecommunications company in South Korea",
            "Pioneer in fiber-to-the-home deployments",
            "Known for ultra-fast broadband speeds",
        ],
    ),
    Network(
        asn=9498,
        name="Bharti Airtel",
        tier=Tier.TIER_2,
        headquarters="New Delhi, India",
        specialization="Indian carrier, Africa presence",
        facts=[
            "Largest mobile operator in India",
            "Significant presence in Africa",
            "Major submarine cable investor",
        ],
    ),
    Network(
        asn=4323,
        name="TW Telecom (Lumen)",
        tier=Tier.TIER_2,
        headquarters="Littleton, Colorado, USA",
        specialization="US enterprise services",
        facts=[
            "Acquired by Level 3 in 2014 (now Lumen)",
            "Focus on enterprise customers",
            "Extensive US metro fiber networks",
        ],
    ),

    # === TIER 3 NETWORKS (Major Regional/National ISPs) ===
    Network(
        asn=7843,
        name="Charter Communications",
        tier=Tier.TIER_3,
        headquarters="Stamford, Connecticut, USA",
        specialization="US cable ISP, Spectrum brand",
        facts=[
            "Second largest cable operator in the US",
            "Operates under Spectrum brand",
            "Formed from Charter/Time Warner Cable merger",
        ],
    ),
    Network(
        asn=22773,
        name="Cox Communications",
        tier=Tier.TIER_3,
        headquarters="Atlanta, Georgia, USA",
        specialization="US cable ISP",
        facts=[
            "Third largest cable company in the US",
            "Privately held company",
            "Focus on residential and business services",
        ],
    ),
    Network(
        asn=5650,
        name="Frontier Communications",
        tier=Tier.TIER_3,
        headquarters="Norwalk, Connecticut, USA",
        specialization="US rural telecommunications",
        facts=[
            "Focus on rural and suburban markets",
            "Acquired Verizon FiOS territories",
            "Emerged from bankruptcy in 2021",
        ],
    ),
    Network(
        asn=20115,
        name="Charter Communications",
        tier=Tier.TIER_3,
        headquarters="Stamford, Connecticut, USA",
        specialization="Spectrum Business services",
        facts=[
            "Business services division of Charter",
            "Enterprise and SMB focus",
            "Separate ASN from residential services",
        ],
    ),
    Network(
        asn=11351,
        name="Road Runner (Spectrum)",
        tier=Tier.TIER_3,
        headquarters="Stamford, Connecticut, USA",
        specialization="Legacy Time Warner Cable network",
        facts=[
            "Historic Time Warner Cable ASN",
            "Now part of Charter/Spectrum",
            "Still used for some legacy infrastructure",
        ],
    ),
    Network(
        asn=11426,
        name="Verizon FiOS",
        tier=Tier.TIER_3,
        headquarters="Basking Ridge, New Jersey, USA",
        specialization="Fiber-to-the-home service",
        facts=[
            "First major US FTTH deployment",
            "Covers northeastern US primarily",
            "Uses GPON technology",
        ],
    ),

    # === CDN PROVIDERS ===
    Network(
        asn=13335,
        name="Cloudflare",
        tier=Tier.CDN,
        headquarters="San Francisco, California, USA",
        specialization="CDN, DDoS protection, DNS",
        facts=[
            "Operates 1.1.1.1 public DNS resolver",
            "Anycast network in 300+ cities",
            "Major DDoS mitigation provider",
            "Founded in 2009",
        ],
    ),
    Network(
        asn=20940,
        name="Akamai Technologies",
        tier=Tier.CDN,
        headquarters="Cambridge, Massachusetts, USA",
        specialization="Largest CDN, edge computing",
        facts=[
            "World's largest CDN by traffic",
            "Founded in 1998 at MIT",
            "Delivers 15-30% of all web traffic",
            "Pioneer in content delivery technology",
        ],
    ),
    Network(
        asn=54113,
        name="Fastly",
        tier=Tier.CDN,
        headquarters="San Francisco, California, USA",
        specialization="Edge cloud platform, real-time CDN",
        facts=[
            "Focus on programmable edge computing",
            "Real-time log streaming",
            "Used by major tech companies",
        ],
    ),
    Network(
        asn=15133,
        name="Edgecast (Edgio)",
        tier=Tier.CDN,
        headquarters="Los Angeles, California, USA",
        specialization="CDN and streaming",
        facts=[
            "Formerly Verizon Digital Media Services",
            "Now part of Edgio (merged with Limelight)",
            "Focus on video streaming",
        ],
    ),
    Network(
        asn=22822,
        name="Limelight Networks (Edgio)",
        tier=Tier.CDN,
        headquarters="Tempe, Arizona, USA",
        specialization="Video delivery, gaming",
        facts=[
            "Merged with Edgecast to form Edgio",
            "Specialized in video delivery",
            "Strong gaming industry presence",
        ],
    ),
    Network(
        asn=2906,
        name="Netflix",
        tier=Tier.CDN,
        headquarters="Los Gatos, California, USA",
        specialization="Open Connect CDN",
        facts=[
            "Operates Open Connect CDN",
            "Deploys cache appliances at ISPs",
            "Accounts for significant Internet traffic",
        ],
    ),
    Network(
        asn=46489,
        name="Twitch",
        tier=Tier.CDN,
        headquarters="San Francisco, California, USA",
        specialization="Live streaming platform",
        facts=[
            "Owned by Amazon",
            "Largest live streaming platform for gaming",
            "Uses own CDN infrastructure",
        ],
    ),

    # === CLOUD PROVIDERS ===
    Network(
        asn=16509,
        name="Amazon Web Services",
        tier=Tier.CLOUD,
        headquarters="Seattle, Washington, USA",
        specialization="Cloud computing, AWS",
        facts=[
            "Largest cloud provider globally",
            "Launched in 2006",
            "Operates CloudFront CDN",
            "Multiple availability zones worldwide",
        ],
    ),
    Network(
        asn=14618,
        name="Amazon.com",
        tier=Tier.CLOUD,
        headquarters="Seattle, Washington, USA",
        specialization="Amazon corporate and retail",
        facts=[
            "Amazon's corporate ASN",
            "Separate from AWS infrastructure",
            "Handles amazon.com traffic",
        ],
    ),
    Network(
        asn=15169,
        name="Google",
        tier=Tier.CLOUD,
        headquarters="Mountain View, California, USA",
        specialization="Google Cloud, Search, YouTube",
        facts=[
            "Operates Google Cloud Platform",
            "YouTube is world's largest video platform",
            "Extensive private fiber network (B4)",
            "Pioneer in SDN and network automation",
        ],
    ),
    Network(
        asn=8075,
        name="Microsoft Azure",
        tier=Tier.CLOUD,
        headquarters="Redmond, Washington, USA",
        specialization="Cloud computing, Office 365",
        facts=[
            "Second largest cloud provider",
            "Operates Azure and Office 365",
            "60+ regions worldwide",
            "Extensive enterprise presence",
        ],
    ),
    Network(
        asn=36351,
        name="IBM Cloud (SoftLayer)",
        tier=Tier.CLOUD,
        headquarters="Dallas, Texas, USA",
        specialization="Enterprise cloud, bare metal",
        facts=[
            "Acquired by IBM in 2013",
            "Focus on enterprise workloads",
            "Bare metal server offerings",
        ],
    ),
    Network(
        asn=45102,
        name="Alibaba Cloud",
        tier=Tier.CLOUD,
        headquarters="Hangzhou, China",
        specialization="Chinese cloud provider",
        facts=[
            "Largest cloud provider in Asia",
            "Part of Alibaba Group",
            "Strong presence in China and Asia-Pacific",
        ],
    ),
    Network(
        asn=13414,
        name="Twitter (X)",
        tier=Tier.CLOUD,
        headquarters="San Francisco, California, USA",
        specialization="Social media platform",
        facts=[
            "Rebranded to X in 2023",
            "Operates own edge infrastructure",
            "High-volume real-time platform",
        ],
    ),
    Network(
        asn=32934,
        name="Meta (Facebook)",
        tier=Tier.CLOUD,
        headquarters="Menlo Park, California, USA",
        specialization="Social media, VR platforms",
        facts=[
            "Operates Facebook, Instagram, WhatsApp",
            "Massive internal network infrastructure",
            "Major submarine cable investor",
            "Developing metaverse platform",
        ],
    ),
    Network(
        asn=714,
        name="Apple",
        tier=Tier.CLOUD,
        headquarters="Cupertino, California, USA",
        specialization="iCloud, App Store, services",
        facts=[
            "Operates iCloud services",
            "Major CDN for App Store and software updates",
            "Uses own and third-party infrastructure",
        ],
    ),
    Network(
        asn=396982,
        name="Google Cloud",
        tier=Tier.CLOUD,
        headquarters="Mountain View, California, USA",
        specialization="Google Cloud Platform dedicated ASN",
        facts=[
            "Dedicated ASN for GCP services",
            "Separate from main Google ASN",
            "Used for cloud customer traffic",
        ],
    ),
    Network(
        asn=19679,
        name="Dropbox",
        tier=Tier.CLOUD,
        headquarters="San Francisco, California, USA",
        specialization="Cloud storage",
        facts=[
            "Migrated from AWS to own infrastructure",
            "Major cloud storage provider",
            "Operates Magic Pocket storage system",
        ],
    ),

    # === INTERNET EXCHANGE POINTS ===
    Network(
        asn=6695,
        name="DE-CIX Frankfurt",
        tier=Tier.IXP,
        headquarters="Frankfurt, Germany",
        specialization="Largest IXP by traffic",
        facts=[
            "World's largest Internet exchange by peak traffic",
            "Over 1000 connected networks",
            "Founded in 1995",
            "Peak traffic over 14 Tbps",
        ],
    ),
    Network(
        asn=1200,
        name="AMS-IX",
        tier=Tier.IXP,
        headquarters="Amsterdam, Netherlands",
        specialization="Major European IXP",
        facts=[
            "One of the oldest IXPs in the world",
            "Founded in 1997",
            "Over 900 connected members",
            "Critical for European Internet traffic",
        ],
    ),
    Network(
        asn=24115,
        name="LINX",
        tier=Tier.IXP,
        headquarters="London, UK",
        specialization="London Internet Exchange",
        facts=[
            "One of the oldest IXPs",
            "Founded in 1994",
            "Multiple locations in London area",
            "Over 950 member ASNs",
        ],
    ),
    Network(
        asn=8674,
        name="Netnod",
        tier=Tier.IXP,
        headquarters="Stockholm, Sweden",
        specialization="Swedish IXP, root DNS operator",
        facts=[
            "Operates i.root-servers.net",
            "Multiple locations across Sweden",
            "Also provides time services",
        ],
    ),
    Network(
        asn=2914,
        name="Japan Network Access Point (JPNAP)",
        tier=Tier.IXP,
        headquarters="Tokyo, Japan",
        specialization="Major Japanese IXP",
        facts=[
            "Largest IXP in Japan",
            "Operated by Internet Multifeed",
            "Critical for Asia-Pacific connectivity",
        ],
    ),
    Network(
        asn=24940,
        name="Hetzner",
        tier=Tier.CLOUD,
        headquarters="Gunzenhausen, Germany",
        specialization="European hosting provider",
        facts=[
            "Popular for affordable dedicated servers",
            "Data centers in Germany and Finland",
            "Known for competitive pricing",
        ],
    ),
    Network(
        asn=13238,
        name="Yandex",
        tier=Tier.CLOUD,
        headquarters="Moscow, Russia",
        specialization="Russian search and cloud",
        facts=[
            "Largest Russian search engine",
            "Operates Yandex Cloud",
            "Major technology company in Russia",
        ],
    ),
    Network(
        asn=14061,
        name="DigitalOcean",
        tier=Tier.CLOUD,
        headquarters="New York City, USA",
        specialization="Developer-focused cloud",
        facts=[
            "Popular with developers and startups",
            "Simple, affordable cloud services",
            "Known for Droplets (VPS)",
        ],
    ),
    Network(
        asn=63949,
        name="Linode (Akamai)",
        tier=Tier.CLOUD,
        headquarters="Philadelphia, Pennsylvania, USA",
        specialization="Developer-focused cloud",
        facts=[
            "Acquired by Akamai in 2022",
            "Founded in 2003",
            "Pioneer in cloud VPS hosting",
        ],
    ),
    Network(
        asn=20473,
        name="Vultr",
        tier=Tier.CLOUD,
        headquarters="Matawan, New Jersey, USA",
        specialization="Cloud compute provider",
        facts=[
            "Global cloud compute platform",
            "32 data center locations",
            "Owned by Constant Company",
        ],
    ),
    Network(
        asn=132203,
        name="Tencent Cloud",
        tier=Tier.CLOUD,
        headquarters="Shenzhen, China",
        specialization="Chinese cloud provider",
        facts=[
            "Part of Tencent Holdings",
            "Operates WeChat infrastructure",
            "Major gaming cloud platform",
        ],
    ),
    Network(
        asn=398324,
        name="Starlink",
        tier=Tier.TIER_3,
        headquarters="Hawthorne, California, USA",
        specialization="Satellite Internet",
        facts=[
            "SpaceX satellite internet service",
            "Low-Earth orbit constellation",
            "Global coverage expanding",
        ],
    ),
]


def get_networks_by_tier(tier: Tier) -> List[Network]:
    """Get all networks belonging to a specific tier."""
    return [n for n in NETWORKS if n.tier == tier]


def get_all_networks() -> List[Network]:
    """Get all networks."""
    return NETWORKS


def get_network_by_asn(asn: int) -> Network | None:
    """Get a network by its ASN."""
    for network in NETWORKS:
        if network.asn == asn:
            return network
    return None

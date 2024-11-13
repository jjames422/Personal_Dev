import Image from 'next/image'
import Link from 'next/link'
import clsx from 'clsx'

import { Container } from '@/components/Container'
import {
  GitHubIcon,
  InstagramIcon,
  LinkedInIcon,
  XIcon,
} from '@/components/SocialIcons'
import portraitImage from '@/images/portrait.jpg'

function SocialLink({ className, href, children, icon: Icon }) {
  return (
    <li className={clsx(className, 'flex')}>
      <Link
        href={href}
        className="group flex text-sm font-medium text-zinc-800 transition hover:text-teal-500 dark:text-zinc-200 dark:hover:text-teal-500"
      >
        <Icon className="h-6 w-6 flex-none fill-zinc-500 transition group-hover:fill-teal-500" />
        <span className="ml-4">{children}</span>
      </Link>
    </li>
  )
}

function MailIcon(props) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        d="M6 5a3 3 0 0 0-3 3v8a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3V8a3 3 0 0 0-3-3H6Zm.245 2.187a.75.75 0 0 0-.99 1.126l6.25 5.5a.75.75 0 0 0 .99 0l6.25-5.5a.75.75 0 0 0-.99-1.126L12 12.251 6.245 7.187Z"
      />
    </svg>
  )
}

function DocumentIcon(props) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...props}>
      <path
        fillRule="evenodd"
        d="M6 2a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8.414a2 2 0 0 0-.586-1.414l-4.414-4.414A2 2 0 0 0 13.586 2H6zm0 2h7v3a1 1 0 0 0 1 1h3v12H6V4zm9 0v2.586L17.414 8H15a1 1 0 0 1-1-1V4z"
      />
    </svg>
  )
}

export const metadata = {
  title: 'About Jonathan M. James',
  description:
    'Jonathan M. James is a technology executive and humanitarian, advancing cybersecurity, disaster response, and youth education in tech.',
}

export default function About() {
  return (
    <Container className="mt-16 sm:mt-32">
      <div className="grid grid-cols-1 gap-y-16 lg:grid-cols-2 lg:grid-rows-[auto_1fr] lg:gap-y-12">
        <div className="lg:pl-20">
          <div className="max-w-xs px-2.5 lg:max-w-none">
            <Image
              src={portraitImage}
              alt=""
              sizes="(min-width: 1024px) 32rem, 20rem"
              className="aspect-square rotate-3 rounded-2xl bg-zinc-100 object-cover dark:bg-zinc-800"
            />
          </div>
        </div>
        <div className="lg:order-first lg:row-span-2">
          <h1 className="text-4xl font-bold tracking-tight text-zinc-800 sm:text-5xl dark:text-zinc-100">
            I’m Jonathan M. James, a technology executive committed to advancing
            cybersecurity, empowering future generations, and delivering
            innovative solutions.
          </h1>
          <div className="mt-6 space-y-7 text-base text-zinc-600 dark:text-zinc-400">
            <p>
              With over 15 years of experience in cybersecurity, disaster
              response, and strategic IT architecture, I’ve built a career
              focused on making a meaningful impact through technology. In
              addition to leading security initiatives at Bank of America, I am
              passionate about empowering youth, supporting underdeveloped
              communities, and advancing disaster relief efforts globally.
            </p>
            <p>
              Through my work with <strong>CyberPatriot</strong>, I mentor young
              students in cybersecurity fundamentals, equipping them with the
              skills to tackle tomorrow's challenges in technology and security.
              This initiative is particularly rewarding as it allows me to
              inspire and prepare the next generation of tech innovators,
              fostering a more secure digital world.
            </p>
            <p>
              I also serve as a key contributor to the{' '}
              <strong>Seeds of Hope</strong> program, focusing on bridging the
              digital divide in underdeveloped countries. By implementing
              sustainable technology solutions and providing access to digital
              education, I work to create opportunities and support economic
              growth in communities that need it most.
            </p>
            <p>
              My experience in crisis management has been invaluable during
              natural disasters, where I have led disaster response efforts
              through the <strong>Lullipop Foundation</strong>. In the aftermath
              of hurricanes and typhoons, I coordinated technology-driven relief
              operations, helping to restore communications, safeguard critical
              data, and ensure community safety. This work has not only
              strengthened my expertise in resilient infrastructure but has also
              underscored the power of technology in rebuilding and supporting
              communities in need.
            </p>
            <p>
              Today, my focus remains on leveraging technology to drive
              meaningful change. As I move into the C-suite, I aim to bring my
              commitment to cybersecurity, innovation, and humanitarian impact
              to a broader platform, ensuring that technology serves as a force
              for good in our world.
            </p>
          </div>
        </div>
        <div className="lg:pl-20">
          <ul role="list">
            <SocialLink href="#" icon={XIcon}>
              Follow on X
            </SocialLink>
            <SocialLink href="#" icon={InstagramIcon} className="mt-4">
              Follow on Instagram
            </SocialLink>
            <SocialLink href="#" icon={GitHubIcon} className="mt-4">
              Follow on GitHub
            </SocialLink>
            <SocialLink href="#" icon={LinkedInIcon} className="mt-4">
              Follow on LinkedIn
            </SocialLink>
            <SocialLink
              href="mailto:jjames422@me.com"
              icon={MailIcon}
              className="mt-8 border-t border-zinc-100 pt-8 dark:border-zinc-700/40"
            >
              jjames422@me.com
            </SocialLink>
            <li className="mt-4">
              <Link
                href="/path-to-resume.pdf"
                className="group inline-flex items-center text-sm font-medium text-zinc-800 dark:text-zinc-200 hover:text-teal-500 dark:hover:text-teal-500"
                target="_blank"
                rel="noopener noreferrer"
              >
                <DocumentIcon className="h-6 w-6 mr-3 fill-zinc-500 transition group-hover:fill-teal-500" />
                Download Resume
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </Container>
  )
}

<script>
	import Observe from './observe.svelte';
	import Content from '$lib/comp/content.svelte';
</script>

<Content>
	<Observe let:intersecting>
		<div class="observe" class:intersecting>
			<strong class="big">About Me</strong>
			<br /><br />
			My name is <strong>Theophilus</strong>, I am a self-taught student of programming and software
			development, and I spend way too much time and money pursuing this interest.
			<br /> <br />
			I spend most of my free time working on building my skillset, contributing to Open Source projects,
			and trying to learn as much as I can. There have been many good people who have assisted me in
			learning this craft, and I try to pay that forward by helping others who may be newer than I.
			<br /> <br />
			I have benefited in massive ways from the work of those who took the time to share their know-how
			on the internet. From various bloggers to programming forums, to the now ubiquitous Stack Overflow,
			I have, in Borg-like fashion, assimilated the experience and college education of some of the biggest
			(and not so big) names in the technology arena. Shamelessly!
			<br /> <br />
			When I’m not writing code or designing, I tend to be playing music (my other passion), exploring
			my surroundings, and doing my best to experience life beyond the code editor.
		</div>
	</Observe>
</Content>

<style>
	.observe {
		opacity: 0;
		transform: translate(0, -500px) scale(0);

		transition: all 1000ms;
		transition-timing-function: cubic-bezier(0.47, 1.64, 0.41, 0.8);

	}
	.intersecting {
		opacity: 1;
		transform: translate(0, 0) scale(1);
	}

	strong {
		color: var(--accent1);
	}
</style>

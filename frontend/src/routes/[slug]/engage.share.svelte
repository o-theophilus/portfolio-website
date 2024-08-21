<script>
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';

	let text = `Check Out: ${$module.post.name}`;
</script>

<section class="content">
	<strong class="ititle"> Share </strong>
	<div class="line">
		<Button
			href="https://www.facebook.com/sharer.php?u={$page.url.href}"
			target="_blank"
			tooltip="Facebook"
		>
			<Icon icon="facebook" size="1.4" />
		</Button>
		<Button
			href="http://twitter.com/share?text={text}&url={$page.url.href}&hashtags=meji,shopping"
			target="_blank"
			tooltip="Twitter"
		>
			<Icon icon="twitter" size="1.4" />
		</Button>

		<Button href="whatsapp://send?text={text}%20{$page.url.href}" tooltip="Whatsapp">
			<Icon icon="whatsapp" size="1.4" />
		</Button>

		<Button
			href="https://telegram.me/share/url?url={$page.url.href}&text={text}"
			target="_blank"
			tooltip="Telegram"
		>
			<Icon icon="telegram" size="1.4" />
		</Button>
	</div>
</section>

<style>
	.content {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		padding: var(--sp3);
	}

	.line {
		display: flex;
		gap: var(--sp1);
	}
</style>

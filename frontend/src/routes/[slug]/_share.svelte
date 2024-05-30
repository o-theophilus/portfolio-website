<script>
	import { page } from '$app/stores';
	import { module } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	let text = `Check Out: ${$module.post.name}`;
</script>

<section class="content">
	<strong class="big"> Share </strong>
	<div class="line">
		<Button
			icon="facebook"
			href="https://www.facebook.com/sharer.php?u={$page.url.href}"
			target="_blank"
			tooltip="Facebook"
		/>
		<Button
			icon="twitter"
			href="http://twitter.com/share?text={text}&url={$page.url.href}&hashtags=meji,shopping"
			target="_blank"
			tooltip="Twitter"
		/>

		<Button
			icon="whatsapp"
			href="whatsapp://send?text={text}%20{$page.url.href}"
			tooltip="Whatsapp"
		/>

		<Button
			icon="telegram"
			href="https://telegram.me/share/url?url={$page.url.href}&text={text}"
			target="_blank"
			tooltip="Telegram"
		/>
	</div>
</section>

<style>
	.content {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);

		padding: var(--sp3);
	}
</style>

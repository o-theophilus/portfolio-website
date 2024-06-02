<script>
	import { page } from '$app/stores';

	export let title;
	export let description;
	export let image = `${$page.url.origin}/image/hero_image.png`;

	title = `${title} | Loup`;
	description = description ? description : title;
</script>

<svelte:head>
	<title>{title}</title>

	<meta name="title" content={title} />
	<meta name="description" content={description} />

	<meta property="og:title" content={title} />
	<meta property="og:description" content={description} />
	<meta property="og:image" content={image} />
	<meta property="og:image:alt" content={title} />
	<meta property="og:url" content={$page.url.href} />
	<meta property="og:type" content="website" />

	<meta name="twitter:title" content={title} />
	<meta name="twitter:description" content={description} />
	<meta name="twitter:image" content={image} />
	<meta name="twitter:image:alt" content={title} />
	<meta name="twitter:url" content={$page.url.href} />
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:site" content="@meji_ng" />
</svelte:head>

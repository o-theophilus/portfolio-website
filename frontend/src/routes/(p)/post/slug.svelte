<script>
	import { api_url, module, _tick, _user } from '$lib/store.js';

	import Content from '$lib/comp/content.svelte';
	import Marked from '$lib/comp/marked.svelte';
	import Meta from '$lib/comp/meta.svelte';
	import Button from '$lib/comp/button.svelte';
	import Tags from '$lib/comp/tags.svelte';

	import Delete from '$lib/module/delete.svelte';
	import Title from '$lib/module/edit_title.svelte';
	import Description from '$lib/module/edit_description.svelte';
	import Edit_Tags from '$lib/module/edit_tags.svelte';
	import Edit_Content from '$lib/module/edit_content.svelte';
	import Edit_Date from '$lib/module/edit_date.svelte';
	import Edit_Status from '$lib/module/edit_status.svelte';
	import Manage_Photo from '$lib/module/manage_photo.svelte';
	import Manage_Video from '$lib/module/manage_video.svelte';

	export let data;
	let { post } = data;
	let { tags } = data;
	let { post_type } = data;

	$: if ($_tick) {
		post = $_tick;
		$_tick = '';
	}

	let content = post.content;
	$: {
		content = post.content;
		post.photo_count = 1;
		let is_available = content.search(/{#photo}/) >= 0;
		while (is_available) {
			let photo = `![${post.title}](${api_url}/${post.photos[post.photo_count]})`;
			content = content.replace(/{#photo}/, photo);
			is_available = content.search(/{#photo}/) >= 0;
			post.photo_count = post.photo_count + 1;
		}
	}

	$: {
		post.video_count = 0;
		let is_available = content.search(/{#video}/) >= 0;
		while (is_available) {
			let v = `<iframe 
					width="100%" 
					height="500px"
					frameborder="0" 
					src="https://www.youtube.com/embed/${post.videos[post.video_count]}">
				</iframe>
				`;
			content = content.replace(/{#video}/, v);
			is_available = content.search(/{#video}/) >= 0;
			post.video_count = post.video_count + 1;
		}
	}
</script>

<Meta title={post.title} description={post.description} image={post.photos[0]} />

<Content>
	<img
		src="{api_url}/{post.photos[0] || ''}"
		alt={post.title}
		onerror="this.src='/site/no_photo.png'"
	/>

	{#if $_user.roles.includes('admin')}
		<br />
		<div class="row">
			<Button
				class="tiny"
				on:click={() => {
					$module = {
						module: Manage_Photo,
						data: {
							post,
							post_type
						}
					};
				}}>Manage Photo</Button
			>
			{#if post.video_count > 0}
				<Button
					class="tiny"
					on:click={() => {
						$module = {
							module: Manage_Video,
							data: {
								post,
								post_type
							}
						};
					}}>Manage Video</Button
				>
			{/if}
		</div>
	{/if}

	<br /><br />
	<strong class="big">{post.title}</strong>
	{#if $_user.roles.includes('admin')}
		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Title,
					data: {
						post,
						post_type
					}
				};
			}}>Edit Title</Button
		>
	{/if}

	<br /><br />
	<span class="date">{post.created_at}</span>
	{#if $_user.roles.includes('admin')}
		<br />
		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Date,
					data: {
						post,
						post_type
					}
				};
			}}>Edit Date</Button
		>
	{/if}

	{#if $_user.roles.includes('admin')}
		<br /><br />
		{post.description}

		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Description,
					data: {
						post,
						post_type
					}
				};
			}}>Edit Description</Button
		>
	{/if}

	<br /><br />
	<Marked md={content} />

	{#if $_user.roles.includes('admin')}
		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Content,
					data: {
						post,
						post_type
					}
				};
			}}>Edit Content</Button
		>
	{/if}

	<br />

	<Tags tags={post.tags} />

	{#if $_user.roles.includes('admin')}
		<br />
		<Button
			class="tiny"
			on:click={() => {
				$module = {
					module: Edit_Tags,
					data: {
						post,
						all_tags: tags,
						post_type
					}
				};
			}}
		>
			Edit Tags
		</Button>
	{/if}

	{#if $_user.roles.includes('admin')}
		<br /> <br />
		{post.status}
		<div class="row">
			<Button
				on:click={() => {
					$module = {
						module: Edit_Status,
						data: {
							post,
							post_type
						}
					};
				}}>Edit Status</Button
			>
			<Button
				on:click={() => {
					$module = {
						module: Delete,
						data: {
							post,
							post_type
						}
					};
				}}>Delete</Button
			>
		</div>
	{/if}
</Content>

<style>
	.big {
		font-size: x-large;
	}
	img {
		background-color: var(--foreground);
	}
</style>
